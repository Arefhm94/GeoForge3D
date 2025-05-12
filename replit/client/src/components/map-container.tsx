import { useEffect, useRef, useState } from "react";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import "leaflet-control-geocoder";
import "leaflet-control-geocoder/dist/Control.Geocoder.css";
import { calculateArea } from "@/lib/calculate-area";
import { downloadBlob } from "@/lib/utils";
import useBuildingFootprints from "@/hooks/use-building-footprints";

interface GeoJSONLayer {
  id: string;
  name: string;
  layer: L.GeoJSON;
}

export default function MapContainer() {
  const mapRef = useRef<L.Map | null>(null);
  const isMapInitializedRef = useRef(false);
  const rectangleRef = useRef<L.Rectangle | null>(null);
  const [selectedArea, setSelectedArea] = useState<number | null>(null);
  const [drawnRectangle, setDrawnRectangle] = useState<L.LatLngBounds | null>(null);
  
  // Variables for rectangle drawing
  const [isDrawing, setIsDrawing] = useState(false);
  const [startPoint, setStartPoint] = useState<L.LatLng | null>(null);
  
  // Drag and drop GeoJSON state
  const [isDragging, setIsDragging] = useState(false);
  const [geoJSONLayers, setGeoJSONLayers] = useState<GeoJSONLayer[]>([]);
  
  // Building footprints functionality
  const { 
    fetchBuildingFootprints, 
    isVisible: buildingsVisible,
    toggleVisibility: toggleBuildingsVisibility,
    currentLayer: buildingsLayer
  } = useBuildingFootprints({
    bounds: drawnRectangle,
    enabled: true
  });
  
  // Setup map when the component mounts
  useEffect(() => {
    // Create map instance if not already created
    if (!mapRef.current) {
      mapRef.current = L.map('mapContainer', {
        center: [37.7749, -122.4194], // San Francisco
        zoom: 13,
        zoomControl: false
      });
      
      // Add zoom control in the bottom left position, offset for the sidebar
      const zoomControl = new L.Control.Zoom({ position: 'bottomleft' });
      zoomControl.addTo(mapRef.current);
      
      // Add a class to the zoom container for styling
      setTimeout(() => {
        const zoomContainer = document.querySelector('.leaflet-control-zoom') as HTMLElement;
        if (zoomContainer) {
          zoomContainer.classList.add('map-zoom-control');
        }
      }, 100);
    }
    
    if (!isMapInitializedRef.current && mapRef.current) {
      const map = mapRef.current;
      isMapInitializedRef.current = true;
      
      // Clear any existing controls to avoid duplicates
      map.eachLayer(layer => {
        if (layer instanceof L.TileLayer) {
          map.removeLayer(layer);
        }
      });
      
      // Create and add base layers
      const osmLayer = L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      }); // Don't add to map yet
      
      // Dark theme map
      const darkLayer = L.tileLayer("https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png", {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
        subdomains: 'abcd',
        maxZoom: 20
      }).addTo(map); // Add as default dark layer
      
      // Light theme map
      const lightLayer = L.tileLayer("https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png", {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
        subdomains: 'abcd',
        maxZoom: 20
      });
      
      const satelliteLabelsLayer = L.layerGroup([
        L.tileLayer(
          "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}", {
            attribution: 'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community'
          }
        ),
        L.tileLayer(
          "https://server.arcgisonline.com/ArcGIS/rest/services/Reference/World_Boundaries_and_Places/MapServer/tile/{z}/{y}/{x}", {
            attribution: 'Tiles &copy; Esri &mdash; Source: Esri, DeLorme, NAVTEQ, USGS, Intermap, iPC, NRCAN, Esri Japan, METI, Esri China (Hong Kong), Esri (Thailand), TomTom, 2012'
          }
        )
      ]);
      
      const topoLayer = L.tileLayer(
        "https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png", {
          attribution: 'Map data: &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, <a href="http://viewfinderpanoramas.org">SRTM</a> | Map style: &copy; <a href="https://opentopomap.org">OpenTopoMap</a> (<a href="https://creativecommons.org/licenses/by-sa/3.0/">CC-BY-SA</a>)'
        }
      );
      
      // Add map layers control as an icon-based dropdown
      const baseLayers = {
        "OpenStreetMap": osmLayer,
        "Dark": darkLayer,
        "Light": lightLayer,
        "Satellite with Labels": satelliteLabelsLayer,
        "Topographic": topoLayer
      };
      
      // Create and add the layer control
      const layerControl = L.control.layers(baseLayers, {}, {
        position: 'bottomright',
        collapsed: true // Make it collapsed by default (shows only the icon)
      }).addTo(map);
      
      // Add location search control
      try {
        const searchControl = new (L.Control as any).Geocoder({
          position: 'topleft',
          defaultMarkGeocode: false,
          placeholder: 'Search for a location...',
          collapsed: true, // Makes it an icon only, expandable on click
          suggestMinLength: 3,
          errorMessage: 'No results found.',
          expand: 'click' // Expand on click
        }).on('markgeocode', function(e: any) {
          const { center, name } = e.geocode;
          
          if (center) {
            map.setView(center, 14);
            L.marker(center)
              .addTo(map)
              .bindPopup(name || 'Selected location')
              .openPopup();
          }
        }).addTo(map);
      } catch (error) {
        console.error("Error initializing geocoder:", error);
      }
      
      // CUSTOM RECTANGLE DRAWING IMPLEMENTATION
      
      // Function to generate GeoJSON from bounds
      const boundsToGeoJSON = (bounds: L.LatLngBounds) => {
        const sw = bounds.getSouthWest();
        const se = bounds.getSouthEast();
        const ne = bounds.getNorthEast();
        const nw = bounds.getNorthWest();
        
        return {
          type: "Feature",
          properties: {},
          geometry: {
            type: "Polygon",
            coordinates: [[
              [sw.lng, sw.lat],
              [se.lng, se.lat],
              [ne.lng, ne.lat],
              [nw.lng, nw.lat],
              [sw.lng, sw.lat] // Close the polygon
            ]]
          }
        };
      };
      
      // Function to handle the start of drawing
      const startDrawingRectangle = () => {
        console.log("Starting rectangle drawing...");
        
        // Reset any existing rectangle
        if (rectangleRef.current && map) {
          map.removeLayer(rectangleRef.current);
          rectangleRef.current = null;
        }
        
        setSelectedArea(null);
        setIsDrawing(false);
        setStartPoint(null);
        
        // Change cursor to crosshair
        map.getContainer().style.cursor = 'crosshair';
        
        // Handler for the first click
        const onFirstClick = (e: L.LeafletMouseEvent) => {
          console.log("First click at:", e.latlng);
          const firstPoint = e.latlng;
          setStartPoint(firstPoint);
          setIsDrawing(true);
          
          let tempRectangle: L.Rectangle | null = null;
          
          // Handler for mousemove to draw rectangle as mouse moves
          const onMouseMove = (moveEvent: L.LeafletMouseEvent) => {
            if (firstPoint) {
              // Remove previous temporary rectangle if it exists
              if (tempRectangle) {
                map.removeLayer(tempRectangle);
              }
              
              // Create rectangle from start point to current mouse position
              const bounds = L.latLngBounds(firstPoint, moveEvent.latlng);
              tempRectangle = L.rectangle(bounds, {
                color: '#0078FF',
                weight: 2,
                opacity: 0.9,
                fillOpacity: 0.2
              }).addTo(map);
              
              // Calculate area
              const area = calculateArea(bounds);
              setSelectedArea(area);
            }
          };
          
          // Handler for second click to complete rectangle
          const onSecondClick = (secondClickEvent: L.LeafletMouseEvent) => {
            console.log("Second click at:", secondClickEvent.latlng);
            
            // Remove event handlers
            map.off('mousemove', onMouseMove);
            map.off('click', onSecondClick);
            
            // Reset drawing state
            setIsDrawing(false);
            map.getContainer().style.cursor = '';
            
            // Remove temporary rectangle
            if (tempRectangle) {
              map.removeLayer(tempRectangle);
            }
            
            // Create the final rectangle
            const bounds = L.latLngBounds(firstPoint, secondClickEvent.latlng);
            const area = calculateArea(bounds);
            
            // Set drawn rectangle bounds for building footprints
            setDrawnRectangle(bounds);
            
            // Get coordinates for display
            const sw = bounds.getSouthWest();
            const se = bounds.getSouthEast();
            const ne = bounds.getNorthEast();
            const nw = bounds.getNorthWest();
            
            // Format coordinates for display
            const formatCoord = (latlng: L.LatLng) => `${latlng.lat.toFixed(6)}, ${latlng.lng.toFixed(6)}`;
            
            const finalRectangle = L.rectangle(bounds, {
              color: '#0078FF',
              weight: 2,
              opacity: 0.9,
              fillOpacity: 0.2
            }).addTo(map);
            
            // Store reference to the rectangle
            rectangleRef.current = finalRectangle;
            
            // Set selected area
            setSelectedArea(area);
            
            // Convert bounds to GeoJSON
            const geoJSON = boundsToGeoJSON(bounds);
            
            // Add visible markers at the corners with coordinates
            const createCornerMarker = (pos: L.LatLng, label: string) => {
              const icon = L.divIcon({
                className: 'coordinate-marker',
                html: `<div class="coordinate-label">${formatCoord(pos)}</div>`,
                iconSize: [6, 6],
                iconAnchor: [3, 3]
              });
              
              return L.marker(pos, { icon }).addTo(map);
            };
            
            const cornerMarkers = [
              createCornerMarker(sw, 'SW'),
              createCornerMarker(se, 'SE'),
              createCornerMarker(ne, 'NE'),
              createCornerMarker(nw, 'NW')
            ];
            
            // Add hover effect to show GeoJSON
            finalRectangle.on('mouseover', function(e) {
              const tooltipContent = `
                <div>
                  <strong>Area:</strong> ${area.toLocaleString()} m²<br/>
                  <strong>Coordinates:</strong><br/>
                  <span style="font-size: 11px;">SW: ${formatCoord(sw)}</span><br/>
                  <span style="font-size: 11px;">SE: ${formatCoord(se)}</span><br/>
                  <span style="font-size: 11px;">NE: ${formatCoord(ne)}</span><br/>
                  <span style="font-size: 11px;">NW: ${formatCoord(nw)}</span><br/>
                  <strong>GeoJSON:</strong><br/>
                  <pre style="max-height: 100px; overflow: auto; font-size: 10px;">${JSON.stringify(geoJSON, null, 2)}</pre>
                </div>
              `;
              
              finalRectangle.bindTooltip(tooltipContent, {
                sticky: true,
                opacity: 0.9,
                className: 'leaflet-tooltip-geojson'
              }).openTooltip();
            });
            
            // Remove tooltip on mouseout
            finalRectangle.on('mouseout', function(e) {
              finalRectangle.closeTooltip();
            });
            
            // Export GeoJSON function
            const exportGeoJSON = () => {
              const geojsonString = JSON.stringify(geoJSON, null, 2);
              const blob = new Blob([geojsonString], { type: 'application/json' });
              downloadBlob(blob, 'rectangle.geojson');
            };
            
            // Remove rectangle function
            const removeRectangle = () => {
              // Remove the rectangle
              map.removeLayer(finalRectangle);
              
              // Remove corner markers
              cornerMarkers.forEach(marker => map.removeLayer(marker));
              
              // Clear the reference
              rectangleRef.current = null;
              
              // Clear the selected area and drawn rectangle state
              setSelectedArea(null);
              setDrawnRectangle(null);
            };
            
            // Add popup with area information and action buttons
            const popupContent = `
              <div class="rectangle-popup">
                <div class="area-info">Area: ${area.toLocaleString()} m²</div>
                <div class="popup-actions">
                  <button class="popup-btn export-btn">Export GeoJSON</button>
                  <button class="popup-btn remove-btn">Remove Rectangle</button>
                </div>
              </div>
            `;
            
            finalRectangle.bindPopup(popupContent);
            
            // Handle click to open popup with actions
            finalRectangle.on('click', function(e) {
              finalRectangle.openPopup();
              
              // Add event listeners after popup is opened
              setTimeout(() => {
                const exportBtn = document.querySelector('.export-btn');
                const removeBtn = document.querySelector('.remove-btn');
                
                if (exportBtn) {
                  exportBtn.addEventListener('click', exportGeoJSON);
                }
                
                if (removeBtn) {
                  removeBtn.addEventListener('click', removeRectangle);
                }
              }, 100);
            });
          };
          
          // Start listening for mouse movement and second click
          map.on('mousemove', onMouseMove);
          map.once('click', onSecondClick);
        };
        
        // Listen for the first click to start drawing
        map.once('click', onFirstClick);
      };
      
      // Create a custom rectangle draw control
      const RectangleDrawControl = L.Control.extend({
        options: {
          position: 'topright'
        },
        
        onAdd: function() {
          const container = L.DomUtil.create('div', 'leaflet-bar leaflet-control leaflet-control-custom');
          container.style.backgroundColor = 'rgba(30, 41, 59, 0.8)';
          container.style.width = '32px';
          container.style.height = '32px';
          container.style.borderRadius = '4px';
          container.style.boxShadow = '0 2px 6px rgba(0,0,0,0.3)';
          container.style.cursor = 'pointer';
          container.style.marginTop = '52px'; // Position below search icon
          container.style.display = 'flex';
          container.style.alignItems = 'center';
          container.style.justifyContent = 'center';
          container.style.transition = 'all 0.2s ease';
          container.style.backdropFilter = 'blur(5px)';
          container.style.border = '1px solid rgba(100, 116, 139, 0.3)';
          
          // Add hover effect
          container.onmouseover = function() {
            container.style.backgroundColor = 'rgba(51, 65, 85, 0.9)';
            container.style.boxShadow = '0 2px 8px rgba(0,0,0,0.4)';
            container.style.transform = 'translateY(-2px)';
          };
          container.onmouseout = function() {
            container.style.backgroundColor = 'rgba(30, 41, 59, 0.8)';
            container.style.boxShadow = '0 2px 6px rgba(0,0,0,0.3)';
            container.style.transform = 'translateY(0)';
          };
          
          // Add icon matching the provided design
          const icon = L.DomUtil.create('div', '', container);
          icon.innerHTML = `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect x="4" y="4" width="16" height="16" stroke="white" strokeWidth="2" fill="none"/>
            <circle cx="4" cy="4" r="2.5" fill="white"/>
            <circle cx="20" cy="4" r="2.5" fill="white"/>
            <circle cx="4" cy="20" r="2.5" fill="white"/>
            <circle cx="20" cy="20" r="2.5" fill="white"/>
          </svg>`;
          
          // Add click event to start drawing
          L.DomEvent.on(container, 'click', function(e: Event) {
            L.DomEvent.stopPropagation(e);
            L.DomEvent.preventDefault(e);
            
            // Start the rectangle drawing process
            startDrawingRectangle();
          });
          
          return container;
        }
      });
      
      // Add the custom rectangle draw control to the map
      new RectangleDrawControl().addTo(map);
    }
    
    // Cleanup on unmount
    return () => {
      if (mapRef.current) {
        // Clean up if needed
      }
    };
  }, [isDrawing, startPoint]);
  
  // Fetch building footprints when rectangle is drawn
  useEffect(() => {
    if (mapRef.current && drawnRectangle && buildingsVisible) {
      fetchBuildingFootprints(mapRef.current);
    }
  }, [drawnRectangle, buildingsVisible, fetchBuildingFootprints]);
  
  // Drag and drop GeoJSON handling
  useEffect(() => {
    if (!mapRef.current) return;
    
    const map = mapRef.current;
    const container = map.getContainer();
    
    // Prevent default browser behavior for drag and drop
    const preventDefaults = (e: Event) => {
      e.preventDefault();
      e.stopPropagation();
    };
    
    // Handle dragenter event
    const handleDragEnter = (e: DragEvent) => {
      preventDefaults(e);
      setIsDragging(true);
    };
    
    // Handle dragleave event
    const handleDragLeave = (e: DragEvent) => {
      preventDefaults(e);
      setIsDragging(false);
    };
    
    // Handle dragover event
    const handleDragOver = (e: DragEvent) => {
      preventDefaults(e);
      setIsDragging(true);
    };
    
    // Handle drop event
    const handleDrop = (e: DragEvent) => {
      preventDefaults(e);
      setIsDragging(false);
      
      if (!e.dataTransfer?.files || e.dataTransfer.files.length === 0) return;
      
      const file = e.dataTransfer.files[0];
      
      // Check if file is a GeoJSON file
      if (file.type !== 'application/geo+json' && !file.name.endsWith('.geojson') && !file.name.endsWith('.json')) {
        alert('Please drop a GeoJSON file (.geojson or .json)');
        return;
      }
      
      // Read the file
      const reader = new FileReader();
      reader.onload = (loadEvent) => {
        try {
          const content = loadEvent.target?.result;
          if (!content) return;
          
          const geoJSON = JSON.parse(content as string);
          
          // Add GeoJSON to map
          const style = {
            color: `rgb(${Math.floor(Math.random() * 155) + 100}, ${Math.floor(Math.random() * 155) + 100}, ${Math.floor(Math.random() * 155) + 100})`,
            weight: 2,
            opacity: 0.8,
            fillOpacity: 0.3
          };
          
          const layer = L.geoJSON(geoJSON, { style }).addTo(map);
          
          // Generate a unique ID
          const layerId = `geojson-${Date.now()}-${Math.floor(Math.random() * 1000)}`;
          
          // Add to layers state
          setGeoJSONLayers(prev => [
            ...prev, 
            { 
              id: layerId, 
              name: file.name,
              layer 
            }
          ]);
          
          // Fit map to the GeoJSON bounds
          const bounds = layer.getBounds();
          if (bounds.isValid()) {
            map.fitBounds(bounds);
          }
        } catch (error) {
          console.error('Error parsing GeoJSON:', error);
          alert('Error parsing GeoJSON file. Please check the file format.');
        }
      };
      
      reader.readAsText(file);
    };
    
    // Add event listeners
    container.addEventListener('dragenter', handleDragEnter);
    container.addEventListener('dragleave', handleDragLeave);
    container.addEventListener('dragover', handleDragOver);
    container.addEventListener('drop', handleDrop);
    
    // Cleanup event listeners
    return () => {
      container.removeEventListener('dragenter', handleDragEnter);
      container.removeEventListener('dragleave', handleDragLeave);
      container.removeEventListener('dragover', handleDragOver);
      container.removeEventListener('drop', handleDrop);
    };
  }, []);
  
  // Handle removing a GeoJSON layer
  const removeGeoJSONLayer = (id: string) => {
    setGeoJSONLayers(prev => {
      // Find the layer to remove
      const layerToRemove = prev.find(layer => layer.id === id);
      
      // Remove from map if found
      if (layerToRemove && mapRef.current) {
        mapRef.current.removeLayer(layerToRemove.layer);
      }
      
      // Return updated state without the removed layer
      return prev.filter(layer => layer.id !== id);
    });
  };
  
  // State for search
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState<Array<{name: string, center: L.LatLng}>>([]);
  const [isSearching, setIsSearching] = useState(false);
  const [isSearchExpanded, setIsSearchExpanded] = useState(false);

  // Handle search submission
  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!searchQuery.trim() || !mapRef.current) return;
    
    setIsSearching(true);
    
    try {
      // Use Nominatim API for geocoding
      const response = await fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(searchQuery)}`);
      const data = await response.json();
      
      if (data && Array.isArray(data) && data.length > 0) {
        // Format the results
        const formattedResults = data.map((item: any) => ({
          name: item.display_name,
          center: L.latLng(parseFloat(item.lat), parseFloat(item.lon))
        }));
        
        setSearchResults(formattedResults);
        
        // If we have results, focus the map on the first one
        if (formattedResults.length > 0 && mapRef.current) {
          mapRef.current.setView(formattedResults[0].center, 14);
          L.marker(formattedResults[0].center)
            .addTo(mapRef.current)
            .bindPopup(formattedResults[0].name)
            .openPopup();
        }
      } else {
        setSearchResults([]);
      }
    } catch (error) {
      console.error("Error searching for location:", error);
      setSearchResults([]);
    }
    
    setIsSearching(false);
  };

  return (
    <div className="absolute inset-0 z-0">
      <div id="mapContainer" className="w-full h-full"></div>
      
      {/* Search bar - collapsible with icon */}
      <div className={`map-search-container ${isSearchExpanded ? 'expanded' : ''}`}>
        {/* Toggle button */}
        <button
          type="button"
          className="map-search-toggle"
          onClick={() => setIsSearchExpanded(!isSearchExpanded)}
          aria-label={isSearchExpanded ? "Collapse search" : "Expand search"}
        >
          <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
        </button>
        
        {/* Search form */}
        <form onSubmit={handleSearch} className="relative">
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search for a location..."
            className="map-search-input"
            aria-expanded={isSearchExpanded}
          />
          <button 
            type="submit" 
            className="map-search-button"
            aria-label="Search"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          </button>
        </form>
        
        {/* Search results */}
        {isSearchExpanded && searchResults.length > 0 && (
          <div className="search-results-container absolute top-full right-0 mt-2 w-60">
            <ul>
              {searchResults.map((result, index) => (
                <li 
                  key={index} 
                  className="search-result-item"
                  onClick={() => {
                    if (mapRef.current) {
                      mapRef.current.setView(result.center, 14);
                      L.marker(result.center)
                        .addTo(mapRef.current)
                        .bindPopup(result.name)
                        .openPopup();
                      setSearchResults([]);
                    }
                  }}
                >
                  {result.name}
                </li>
              ))}
            </ul>
          </div>
        )}
        
        {/* Loading indicator */}
        {isSearchExpanded && isSearching && (
          <div className="search-results-container absolute top-full right-0 mt-2 w-60">
            <div className="search-result-item text-center">
              <div className="flex items-center justify-center">
                <svg className="animate-spin h-5 w-5 mr-2 text-blue-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Searching...
              </div>
            </div>
          </div>
        )}
      </div>
      
      {/* Area display */}
      {selectedArea && (
        <div className="absolute bottom-4 right-4 z-10 px-3 py-2 rounded-md area-info-display text-sm">
          <div className="flex items-center space-x-2">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <rect x="3" y="3" width="18" height="18" rx="2" stroke="#3498db" strokeWidth="2"/>
            </svg>
            <span>
              <span className="font-medium">Area:</span> {selectedArea.toLocaleString()} m²
            </span>
          </div>
        </div>
      )}
      
      {/* Invisible drag overlay that shows only when dragging files */}
      {isDragging && (
        <div className="fixed inset-0 bg-blue-700/30 backdrop-blur-lg z-50 flex items-center justify-center">
          <div className="bg-slate-800/80 backdrop-blur-xl p-6 rounded-lg shadow-lg text-center border border-blue-400/30">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-12 w-12 mx-auto mb-4 text-blue-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
              <polyline points="17 8 12 3 7 8" />
              <line x1="12" y1="3" x2="12" y2="15" />
            </svg>
            <p className="text-lg font-medium text-white">Drop GeoJSON file to import</p>
          </div>
        </div>
      )}
      
      {/* GeoJSON Layers List */}
      {geoJSONLayers.length > 0 && (
        <div className="geojson-layer-controls">
          {geoJSONLayers.map(layer => (
            <div key={layer.id} className="geojson-layer-item">
              <div className="geojson-layer-name" title={layer.name}>
                {layer.name}
              </div>
              <div className="flex items-center gap-1">
                <button 
                  className="geojson-layer-btn" 
                  onClick={() => {
                    // Zoom to this layer
                    if (mapRef.current) {
                      const bounds = layer.layer.getBounds();
                      if (bounds.isValid()) {
                        mapRef.current.fitBounds(bounds);
                      }
                    }
                  }}
                  title="Zoom to layer"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <circle cx="11" cy="11" r="8" />
                    <line x1="21" y1="21" x2="16.65" y2="16.65" />
                    <line x1="11" y1="8" x2="11" y2="14" />
                    <line x1="8" y1="11" x2="14" y2="11" />
                  </svg>
                </button>
                <button 
                  className="geojson-layer-btn" 
                  onClick={() => removeGeoJSONLayer(layer.id)}
                  title="Remove layer"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <line x1="18" y1="6" x2="6" y2="18" />
                    <line x1="6" y1="6" x2="18" y2="18" />
                  </svg>
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}