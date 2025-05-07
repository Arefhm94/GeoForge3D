import { useEffect, useState } from 'react';
import L from 'leaflet';
import { getQueryFn } from '../lib/queryClient';
import { useQuery } from '@tanstack/react-query';

interface BuildingFootprintsProps {
  bounds: L.LatLngBounds | null;
  sources?: string[];
  enabled?: boolean;
}

export default function useBuildingFootprints({
  bounds,
  sources = ['osm', 'microsoft'],
  enabled = false
}: BuildingFootprintsProps) {
  const [isVisible, setIsVisible] = useState(false);
  const [currentLayer, setCurrentLayer] = useState<L.GeoJSON | null>(null);

  // Prepare the query for fetching building footprints
  const buildingsQuery = useQuery({
    queryKey: ['/api/buildings', bounds?.toBBoxString()],
    queryFn: getQueryFn({ on401: 'throw' }),
    enabled: enabled && !!bounds && isVisible,
    refetchOnWindowFocus: false,
    retry: 1,
  });

  const toggleVisibility = () => {
    setIsVisible(!isVisible);
  };

  // Create a function to fetch building footprints
  const fetchBuildingFootprints = async (map: L.Map) => {
    if (!bounds) return;

    try {
      // Clear any existing layer
      if (currentLayer) {
        map.removeLayer(currentLayer);
        setCurrentLayer(null);
      }

      if (!isVisible) return;

      // Get the bounds
      const north = bounds.getNorth();
      const south = bounds.getSouth();
      const east = bounds.getEast();
      const west = bounds.getWest();

      // Prepare API URL
      const sourcesParam = sources.join(',');
      const url = `/api/buildings?north=${north}&south=${south}&east=${east}&west=${west}&sources=${sourcesParam}`;

      // Fetch the data
      const response = await fetch(url);
      if (!response.ok) {
        throw new Error(`Failed to fetch building footprints: ${response.statusText}`);
      }

      const data = await response.json();

      // Create a GeoJSON layer with the footprints
      const geoJsonLayer = L.geoJSON(data, {
        style: (feature) => {
          // Different styles for different sources
          const source = feature?.properties?.source || '';
          
          if (source.includes('Microsoft')) {
            return {
              color: '#3388ff',
              weight: 1,
              fillColor: '#3388ff',
              fillOpacity: 0.3
            };
          } else {
            return {
              color: '#ff4433',
              weight: 1,
              fillColor: '#ff4433',
              fillOpacity: 0.3
            };
          }
        },
        onEachFeature: (feature, layer) => {
          // Add a popup with building information
          const props = feature.properties || {};
          let popupContent = '<div class="building-popup">';
          
          // Add a title based on the source
          if (props.source) {
            popupContent += `<h3>${props.source}</h3>`;
          }
          
          // Add building name if available
          if (props.name) {
            popupContent += `<p><strong>Name:</strong> ${props.name}</p>`;
          }
          
          // Add building type if available
          if (props.building) {
            popupContent += `<p><strong>Type:</strong> ${props.building}</p>`;
          }
          
          // Add address if available
          if (props.addr_housenumber || props.addr_street) {
            popupContent += '<p><strong>Address:</strong> ';
            if (props.addr_housenumber) popupContent += props.addr_housenumber + ' ';
            if (props.addr_street) popupContent += props.addr_street;
            popupContent += '</p>';
          }
          
          // Add building levels if available
          if (props.building_levels) {
            popupContent += `<p><strong>Levels:</strong> ${props.building_levels}</p>`;
          }
          
          // Add OSM ID if available
          if (props.id) {
            popupContent += `<p><strong>ID:</strong> ${props.id}</p>`;
          }
          
          popupContent += '</div>';
          
          layer.bindPopup(popupContent);
        }
      });

      // Add the layer to the map
      geoJsonLayer.addTo(map);
      setCurrentLayer(geoJsonLayer);

    } catch (error) {
      console.error('Error fetching building footprints:', error);
    }
  };

  return {
    buildingsQuery,
    fetchBuildingFootprints,
    isVisible,
    toggleVisibility,
    currentLayer
  };
}