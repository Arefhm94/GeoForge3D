import { useState, useEffect } from "react";
import Sidebar from "@/components/sidebar";
import MapContainer from "@/components/map-container";
import { 
  faLayerGroup, 
  faMountain, 
  faWater, 
  faSeedling, 
  faBuilding, 
  faTree 
} from "@fortawesome/free-solid-svg-icons";

import { IconDefinition } from "@fortawesome/fontawesome-svg-core";

export type AnalysisModule = {
  id: string;
  name: string;
  icon: IconDefinition;
  description: string;
  isActive: boolean;
};

export default function MapPage() {
  const [sidebarExpanded, setSidebarExpanded] = useState(true);
  const [analysisModules, setAnalysisModules] = useState<AnalysisModule[]>([
    {
      id: "land-cover",
      name: "Land Cover Analysis",
      icon: faLayerGroup,
      description: "Analyze land cover composition within selected area.",
      isActive: true,
    },
    {
      id: "elevation",
      name: "Elevation Profile",
      icon: faMountain,
      description: "Calculate elevation statistics for selected area.",
      isActive: false,
    },
    {
      id: "water-detection",
      name: "Water Detection",
      icon: faWater,
      description: "Identify water bodies and calculate water coverage.",
      isActive: false,
    },
    {
      id: "vegetation",
      name: "Vegetation Index",
      icon: faSeedling,
      description: "Calculate vegetation health and density metrics.",
      isActive: false,
    },
    {
      id: "urban",
      name: "Urban Footprint",
      icon: faBuilding,
      description: "Detect buildings and urban infrastructure.",
      isActive: false,
    },
    {
      id: "green-areas",
      name: "Green Areas",
      icon: faTree,
      description: "Analyze parks, forests, and other green spaces.",
      isActive: false,
    },
    {
      id: "buildings",
      name: "Building Detection",
      icon: faBuilding,
      description: "Identify and analyze buildings and structures.",
      isActive: false,
    },
    {
      id: "terrain",
      name: "Terrain Analysis",
      icon: faMountain,
      description: "Analyze terrain features and landscape morphology.",
      isActive: false,
    },
  ]);

  const toggleModuleActive = (id: string) => {
    setAnalysisModules((prev) =>
      prev.map((module) => ({
        ...module,
        isActive: module.id === id ? !module.isActive : module.isActive,
      }))
    );
  };
  
  // Add or remove the sidebar-collapsed class to the body element
  // This will be used for responsive positioning of other elements
  const toggleSidebarExpanded = () => {
    if (sidebarExpanded) {
      document.body.classList.add('sidebar-collapsed');
    } else {
      document.body.classList.remove('sidebar-collapsed');
    }
    setSidebarExpanded(!sidebarExpanded);
  };
  
  // Set initial sidebar class and clean up on unmount
  useEffect(() => {
    // Set initial state
    if (!sidebarExpanded) {
      document.body.classList.add('sidebar-collapsed');
    }
    
    // Clean up on unmount
    return () => {
      document.body.classList.remove('sidebar-collapsed');
    };
  }, []);

  return (
    <div className="relative h-screen w-full overflow-hidden">
      <MapContainer />
      
      <div className="absolute top-0 left-0 h-full z-10">
        <Sidebar 
          modules={analysisModules}
          expanded={sidebarExpanded}
          onToggleModule={toggleModuleActive}
          onToggleExpanded={toggleSidebarExpanded}
          onRunAnalysis={() => {
            // Run analysis functionality
          }}
        />
      </div>
    </div>
  );
}