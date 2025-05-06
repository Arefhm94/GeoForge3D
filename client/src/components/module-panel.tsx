import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faChevronUp, faChevronDown } from "@fortawesome/free-solid-svg-icons";
import { IconDefinition } from "@fortawesome/fontawesome-svg-core";
import { Button } from "@/components/ui/button";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { useState } from "react";

interface ModulePanelProps {
  id: string;
  name: string;
  icon: IconDefinition;
  description: string;
  isActive: boolean;
  onToggle: () => void;
  expanded: boolean;
  onRunAnalysis: () => void;
}

export default function ModulePanel({ 
  id, 
  name, 
  icon, 
  description, 
  isActive, 
  onToggle, 
  expanded,
  onRunAnalysis
}: ModulePanelProps) {
  const [resolution, setResolution] = useState("high");
  const [classificationType, setClassificationType] = useState("basic");
  
  if (!expanded) {
    return (
      <div className="mb-2 rounded-lg border border-blue-400/20 overflow-hidden shadow-sm hover:shadow-md transition-all duration-150">
        <div 
          className="bg-slate-900/90 backdrop-blur-md p-2 flex justify-center items-center cursor-pointer hover:bg-slate-700/80"
          onClick={onToggle}
        >
          <FontAwesomeIcon icon={icon} className="text-blue-300" size="xs" />
        </div>
      </div>
    );
  }
  
  return (
    <div className={`module-panel mb-2 rounded-lg border border-blue-400/20 overflow-hidden shadow-sm hover:shadow-md transition-all duration-150 ${isActive ? 'active' : ''}`}>
      <div 
        className="module-header bg-slate-900/90 backdrop-blur-md p-2 flex justify-between items-center cursor-pointer hover:bg-slate-700/80"
        onClick={onToggle}
      >
        <div className="flex items-center">
          <FontAwesomeIcon icon={icon} className="text-blue-300 mr-2 icon" size="sm" />
          <h3 className="font-medium text-slate-100 text-sm">{name}</h3>
        </div>
        <FontAwesomeIcon 
          icon={isActive ? faChevronUp : faChevronDown} 
          className="text-slate-400"
          size="xs"
        />
      </div>
      
      {isActive && (
        <div className="module-content bg-slate-800/80 backdrop-blur-md p-3 border-t border-slate-700/30">
          <p className="text-xs text-slate-300 mb-2">{description}</p>
          <div className="space-y-2">
            {id === "land-cover" && (
              <>
                <div>
                  <label className="block text-xs font-medium text-slate-200 mb-1">Resolution</label>
                  <Select
                    value={resolution}
                    onValueChange={setResolution}
                  >
                    <SelectTrigger className="w-full h-8 text-xs bg-slate-700/80 text-slate-200 border-slate-600">
                      <SelectValue placeholder="Select resolution" />
                    </SelectTrigger>
                    <SelectContent className="bg-slate-800 text-slate-200 border-slate-600">
                      <SelectItem value="high">High (10m)</SelectItem>
                      <SelectItem value="medium">Medium (30m)</SelectItem>
                      <SelectItem value="low">Low (100m)</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div>
                  <label className="block text-xs font-medium text-slate-200 mb-1">Classification Type</label>
                  <div className="flex space-x-1">
                    <button 
                      className={`flex-1 px-2 py-1 rounded-md text-xs ${
                        classificationType === "basic" 
                          ? "bg-blue-500 text-white" 
                          : "bg-slate-700 border border-slate-600 text-slate-200"
                      }`}
                      onClick={() => setClassificationType("basic")}
                    >
                      Basic
                    </button>
                    <button 
                      className={`flex-1 px-2 py-1 rounded-md text-xs ${
                        classificationType === "detailed" 
                          ? "bg-blue-500 text-white" 
                          : "bg-slate-700 border border-slate-600 text-slate-200"
                      }`}
                      onClick={() => setClassificationType("detailed")}
                    >
                      Detailed
                    </button>
                  </div>
                </div>
              </>
            )}
            <Button
              className="w-full bg-blue-500 hover:bg-blue-600 h-8 text-xs"
              onClick={onRunAnalysis}
            >
              Run Analysis
            </Button>
          </div>
        </div>
      )}
    </div>
  );
}
