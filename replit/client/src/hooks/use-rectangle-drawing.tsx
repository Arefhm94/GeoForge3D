import { useState, useEffect, MutableRefObject } from "react";
import L, { LatLngBounds } from "leaflet";
import { calculateArea } from "@/lib/calculate-area";

interface UseRectangleDrawingProps {
  mapRef: MutableRefObject<L.Map>;
  setSelectedArea: (area: number) => void;
  setDrawnRectangle: (bounds: LatLngBounds | null) => void;
}

export default function useRectangleDrawing({ 
  mapRef, 
  setSelectedArea, 
  setDrawnRectangle 
}: UseRectangleDrawingProps) {
  const [drawingEnabled, setDrawingEnabled] = useState(false);
  const [isDrawing, setIsDrawing] = useState(false);
  const [startPoint, setStartPoint] = useState<L.LatLng | null>(null);
  const [rectangle, setRectangle] = useState<L.Rectangle | null>(null);
  
  // Clean up rectangle when component unmounts
  useEffect(() => {
    return () => {
      if (rectangle && mapRef.current) {
        mapRef.current.removeLayer(rectangle);
      }
    };
  }, [rectangle, mapRef]);
  
  const toggleDrawing = () => {
    setDrawingEnabled(!drawingEnabled);
    
    if (mapRef.current) {
      if (!drawingEnabled) {
        mapRef.current.getContainer().style.cursor = "crosshair";
      } else {
        mapRef.current.getContainer().style.cursor = "";
      }
    }
  };
  
  const clearDrawing = () => {
    if (rectangle && mapRef.current) {
      mapRef.current.removeLayer(rectangle);
    }
    
    setRectangle(null);
    setSelectedArea(0);
    setDrawnRectangle(null);
  };
  
  const handleMapClick = (e: L.LeafletMouseEvent) => {
    if (!drawingEnabled) return;
    
    if (!isDrawing) {
      setIsDrawing(true);
      setStartPoint(e.latlng);
    } else {
      setIsDrawing(false);
      setDrawingEnabled(false);
      
      if (mapRef.current) {
        mapRef.current.getContainer().style.cursor = "";
      }
    }
  };
  
  const handleMapMove = (e: L.LeafletMouseEvent) => {
    if (!isDrawing || !drawingEnabled || !startPoint) return;
    
    if (rectangle && mapRef.current) {
      mapRef.current.removeLayer(rectangle);
    }
    
    const bounds = L.latLngBounds(startPoint, e.latlng);
    const newRectangle = L.rectangle(bounds, {
      color: "#3B82F6",
      weight: 2,
      fillOpacity: 0.2
    }).addTo(mapRef.current);
    
    setRectangle(newRectangle);
    
    // Calculate area
    const area = calculateArea(bounds);
    setSelectedArea(area);
    setDrawnRectangle(bounds);
  };
  
  return {
    drawingEnabled,
    toggleDrawing,
    clearDrawing,
    handleMapClick,
    handleMapMove
  };
}
