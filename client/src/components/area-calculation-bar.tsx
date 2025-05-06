import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faInfoCircle } from "@fortawesome/free-solid-svg-icons";

interface AreaCalculationBarProps {
  area: number;
}

export default function AreaCalculationBar({ area }: AreaCalculationBarProps) {
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
  
  return (
    <div className="bg-white border-t border-gray-200 p-3 flex justify-between items-center">
      <div className="flex items-center space-x-4">
        <div>
          <span className="text-sm text-gray-500">Selected Area:</span>
          <span className="font-medium ml-1">{area} m²</span>
        </div>
        
        {isPricing && (
          <div>
            <span className="text-sm text-gray-500">Additional Cost:</span>
            <span className="font-medium ml-1 text-primary">${price.toFixed(2)}</span>
            <span className="text-xs text-gray-500 ml-1">
              (First {getFreeArea()}m² free, then ${getCostPerExtraChunk().toFixed(2)} per {getExtraChunkSize()}m²)
            </span>
          </div>
        )}
      </div>
      
      <div className="text-sm text-gray-500">
        <FontAwesomeIcon icon={faInfoCircle} className="mr-1 text-gray-400" />
        {area === 0 
          ? "Draw a rectangle on the map to select an area" 
          : "Selected area shown on map"}
      </div>
    </div>
  );
}
