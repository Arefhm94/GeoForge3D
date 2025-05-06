import { useEffect, MutableRefObject, useState } from "react";
import L from "leaflet";
import "esri-leaflet";

interface UseMapLayersProps {
  mapRef: MutableRefObject<L.Map | null>;
}

// Define base layer type
type BaseLayerName = "OpenStreetMap" | "Dark" | "Light" | "Satellite with Labels" | "Topographic";

// Add type declaration for Esri Leaflet
declare global {
  namespace L {
    namespace esri {
      function basemapLayer(id: string, options?: any): L.Layer;
    }
    interface Control {
      Layers: new (baseLayers: Record<string, L.Layer>, overlays?: Record<string, L.Layer>, options?: any) => L.Control;
    }
  }
}

export default function useMapLayers({ mapRef }: UseMapLayersProps) {
  const [currentBaseLayer, setCurrentBaseLayer] = useState<BaseLayerName>("Dark");
  const [baseLayers, setBaseLayers] = useState<Partial<Record<BaseLayerName, L.Layer>>>({});
  const [layerControl, setLayerControl] = useState<L.Control | null>(null);

  useEffect(() => {
    if (!mapRef.current) return;
    
    console.log("Initializing map layers");

    // Create base layers
    const osmLayer = L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    });

    // Dark theme map
    const darkLayer = L.tileLayer("https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png", {
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
      subdomains: 'abcd',
      maxZoom: 20
    });

    // Light theme map
    const lightLayer = L.tileLayer("https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png", {
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
      subdomains: 'abcd',
      maxZoom: 20
    });

    // Satellite imagery with labels
    const esriWorldImageryWithLabels = L.layerGroup([
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

    // Topographic map
    const topoLayer = L.tileLayer(
      "https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png", {
        attribution: 'Map data: &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, <a href="http://viewfinderpanoramas.org">SRTM</a> | Map style: &copy; <a href="https://opentopomap.org">OpenTopoMap</a> (<a href="https://creativecommons.org/licenses/by-sa/3.0/">CC-BY-SA</a>)'
      }
    );

    // Create the collection of base layers
    const newBaseLayers = {
      "OpenStreetMap": osmLayer,
      "Dark": darkLayer,
      "Light": lightLayer,
      "Satellite with Labels": esriWorldImageryWithLabels,
      "Topographic": topoLayer
    };

    setBaseLayers(newBaseLayers);

    // Remove any existing base layers from the map
    mapRef.current.eachLayer((layer) => {
      if (layer instanceof L.TileLayer) {
        mapRef.current?.removeLayer(layer);
      }
    });

    // Add the default base layer to the map
    if (mapRef.current) {
      newBaseLayers[currentBaseLayer].addTo(mapRef.current);
    }

    // Add layer control
    if (mapRef.current) {
      const control = L.control.layers(newBaseLayers, {}, {
        position: 'bottomright',
        collapsed: false // Show the control expanded
      }).addTo(mapRef.current);
      
      // Add classes manually since the option isn't supported in TypeScript definitions
      const controlContainer = control.getContainer();
      if (controlContainer) {
        controlContainer.className += ' leaflet-control-layers-custom';
      }
      
      setLayerControl(control);
    }

    return () => {
      if (mapRef.current && layerControl) {
        mapRef.current.removeControl(layerControl);
      }
    };
  }, [mapRef]);

  // Switch base layer
  const switchBaseLayer = (layerName: BaseLayerName) => {
    if (!mapRef.current || !baseLayers[layerName] || layerName === currentBaseLayer) return;

    // Remove current base layer
    (Object.keys(baseLayers) as BaseLayerName[]).forEach(name => {
      const layer = baseLayers[name];
      if (mapRef.current && layer && mapRef.current.hasLayer(layer)) {
        mapRef.current.removeLayer(layer);
      }
    });

    // Add new base layer
    const newLayer = baseLayers[layerName];
    if (newLayer && mapRef.current) {
      newLayer.addTo(mapRef.current);
      setCurrentBaseLayer(layerName);
    }
  };

  return {
    currentBaseLayer,
    switchBaseLayer,
    baseLayers,
    layerControl
  };
}