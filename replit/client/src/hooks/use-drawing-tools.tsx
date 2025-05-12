import { useState, useEffect, MutableRefObject } from "react";
import L from "leaflet";
import "leaflet-draw";
import { calculateArea } from "@/lib/calculate-area";

// This is to fix a TypeScript issue with leaflet-draw
declare module "leaflet" {
  interface Map {
    drawControl?: L.Control;
  }
}

interface UseDrawingToolsProps {
  mapRef: MutableRefObject<L.Map | null>;
  setSelectedArea: (area: number) => void;
  setDrawnRectangle: (bounds: L.LatLngBounds | null) => void;
}

export default function useDrawingTools({
  mapRef,
  setSelectedArea,
  setDrawnRectangle
}: UseDrawingToolsProps) {
  const [drawnItems, setDrawnItems] = useState<L.FeatureGroup | null>(null);

  useEffect(() => {
    if (!mapRef.current) return;
    
    console.log("Initializing drawing tools");

    // Initialize the FeatureGroup to store drawn items
    const newDrawnItems = new L.FeatureGroup();
    mapRef.current.addLayer(newDrawnItems);
    setDrawnItems(newDrawnItems);

    // Initialize the draw control and add it to the map
    const drawControl = new L.Control.Draw({
      position: 'topright',
      draw: {
        polyline: false,  // Disable polyline drawing
        polygon: {
          allowIntersection: false,
          showArea: true,
          drawError: {
            color: '#e1e100',
            message: '<strong>Cannot draw this shape!</strong>'
          },
          shapeOptions: {
            color: '#3388ff',
            weight: 2
          }
        },
        circle: false,  // Disable circle drawing
        circlemarker: false,  // Disable circle marker drawing
        rectangle: {
          shapeOptions: {
            color: '#3388ff',
            weight: 2,
            opacity: 0.7,
            fillOpacity: 0.2
          }
        },
        marker: {}  // Enable marker drawing with default options
      },
      edit: {
        featureGroup: newDrawnItems
      }
    });
    
    mapRef.current.addControl(drawControl);
    
    // Store the control reference
    if (mapRef.current) {
      mapRef.current.drawControl = drawControl;
    }

    return () => {
      if (mapRef.current) {
        if (mapRef.current.drawControl) {
          mapRef.current.removeControl(mapRef.current.drawControl);
          delete mapRef.current.drawControl;
        }
        
        if (drawnItems) {
          mapRef.current.removeLayer(drawnItems);
        }
      }
    };
  }, [mapRef]);

  useEffect(() => {
    if (!mapRef.current || !drawnItems) return;

    // Handle created items
    const handleCreated = (e: any) => {
      drawnItems.addLayer(e.layer);
      
      if (e.layerType === 'rectangle') {
        const bounds = e.layer.getBounds() as L.LatLngBounds;
        const area = calculateArea(bounds);
        setSelectedArea(area);
        setDrawnRectangle(bounds);
      }
    };

    // Handle edited items
    const handleEdited = (e: any) => {
      const layers = e.layers;
      layers.eachLayer((layer: any) => {
        if (layer instanceof L.Rectangle) {
          const bounds = layer.getBounds();
          const area = calculateArea(bounds);
          setSelectedArea(area);
          setDrawnRectangle(bounds);
        }
      });
    };

    // Handle deleted items
    const handleDeleted = () => {
      setSelectedArea(0);
      setDrawnRectangle(null);
    };

    // Add event handlers
    mapRef.current.on(L.Draw.Event.CREATED, handleCreated);
    mapRef.current.on(L.Draw.Event.EDITED, handleEdited);
    mapRef.current.on(L.Draw.Event.DELETED, handleDeleted);

    return () => {
      if (mapRef.current) {
        mapRef.current.off(L.Draw.Event.CREATED, handleCreated);
        mapRef.current.off(L.Draw.Event.EDITED, handleEdited);
        mapRef.current.off(L.Draw.Event.DELETED, handleDeleted);
      }
    };
  }, [mapRef, drawnItems, setSelectedArea, setDrawnRectangle]);

  return {
    drawnItems,
    clearDrawings: () => {
      if (drawnItems) {
        drawnItems.clearLayers();
        setSelectedArea(0);
        setDrawnRectangle(null);
      }
    }
  };
}