import { useState } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faInfoCircle } from "@fortawesome/free-solid-svg-icons";
import { Dialog, DialogContent, DialogHeader, DialogFooter, DialogTitle } from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { LatLngBounds } from "leaflet";

interface ExportModalProps {
  area: number;
  bounds: LatLngBounds;
  onClose: () => void;
}

export default function ExportModal({ area, bounds, onClose }: ExportModalProps) {
  const [filename, setFilename] = useState("area_export.geojson");
  const [format, setFormat] = useState("geojson");
  const [coordSystem, setCoordSystem] = useState("wgs84");
  
  const getFreeArea = () => 100;
  const getCostPerExtraChunk = () => 0.1;
  const getExtraChunkSize = () => 10;
  
  const calculatePrice = () => {
    if (area <= getFreeArea()) return 0;
    
    const extraArea = area - getFreeArea();
    const extraChunks = Math.ceil(extraArea / getExtraChunkSize());
    return extraChunks * getCostPerExtraChunk();
  };
  
  const price = calculatePrice();
  const isPricing = area > getFreeArea();
  
  const exportGeoJSON = () => {
    const geojson = {
      type: "Feature",
      properties: {},
      geometry: {
        type: "Polygon",
        coordinates: [[
          [bounds.getWest(), bounds.getSouth()],
          [bounds.getEast(), bounds.getSouth()],
          [bounds.getEast(), bounds.getNorth()],
          [bounds.getWest(), bounds.getNorth()],
          [bounds.getWest(), bounds.getSouth()]
        ]]
      }
    };
    
    const blob = new Blob([JSON.stringify(geojson)], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = filename || "area_export.geojson";
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    
    onClose();
  };
  
  return (
    <Dialog open={true} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-md">
        <DialogHeader>
          <DialogTitle>Export GeoJSON</DialogTitle>
        </DialogHeader>
        
        <div className="py-4">
          <p className="text-gray-600 mb-4">Your selected area is <span className="font-medium">{area} m²</span>.</p>
          
          {isPricing && (
            <div className="bg-blue-50 border border-blue-200 rounded-md p-3 mb-4">
              <div className="flex items-start">
                <FontAwesomeIcon icon={faInfoCircle} className="text-primary mt-0.5 mr-3" />
                <div>
                  <p className="text-gray-700 text-sm">This area exceeds the free tier of {getFreeArea()}m².</p>
                  <p className="text-gray-700 text-sm mt-1">Additional cost: <span className="font-medium">${price.toFixed(2)}</span></p>
                  <p className="text-xs text-gray-500 mt-1">(${getCostPerExtraChunk().toFixed(2)} per {getExtraChunkSize()}m² over the free limit)</p>
                </div>
              </div>
            </div>
          )}
          
          <div className="mb-4">
            <Label htmlFor="filename">Filename</Label>
            <Input 
              id="filename" 
              value={filename} 
              onChange={(e) => setFilename(e.target.value)} 
              className="mt-1"
            />
          </div>
          
          <div className="flex justify-between gap-4">
            <div className="flex-1">
              <Label htmlFor="format">Format</Label>
              <Select value={format} onValueChange={setFormat}>
                <SelectTrigger id="format" className="mt-1">
                  <SelectValue placeholder="Select format" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="geojson">GeoJSON</SelectItem>
                  <SelectItem value="shapefile">Shapefile</SelectItem>
                  <SelectItem value="kml">KML</SelectItem>
                </SelectContent>
              </Select>
            </div>
            
            <div className="flex-1">
              <Label htmlFor="coordSystem">Coordinate System</Label>
              <Select value={coordSystem} onValueChange={setCoordSystem}>
                <SelectTrigger id="coordSystem" className="mt-1">
                  <SelectValue placeholder="Select coordinate system" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="wgs84">WGS 84 (EPSG:4326)</SelectItem>
                  <SelectItem value="mercator">Web Mercator (EPSG:3857)</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
        </div>
        
        <DialogFooter className="sm:justify-end gap-2">
          <Button variant="outline" onClick={onClose}>
            Cancel
          </Button>
          <Button onClick={exportGeoJSON}>
            Export
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
