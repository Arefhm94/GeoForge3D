import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { 
  faChevronLeft, 
  faChevronRight
} from "@fortawesome/free-solid-svg-icons";
import ModulePanel from "./module-panel";
import type { AnalysisModule } from "@/pages/home";

interface SidebarProps {
  modules: AnalysisModule[];
  expanded: boolean;
  onToggleModule: (id: string) => void;
  onToggleExpanded: () => void;
  onRunAnalysis: () => void;
}

export default function Sidebar({ 
  modules, 
  expanded, 
  onToggleModule, 
  onToggleExpanded,
  onRunAnalysis
}: SidebarProps) {
  return (
    <aside 
      className={`sidebar-container bg-slate-900/80 backdrop-blur-md border border-blue-400/20 flex flex-col h-full transition-all duration-300 shadow-lg rounded-xl ${
        expanded ? "w-64" : "w-14 sidebar-collapsed"
      }`}
      style={{
        marginLeft: "8px",
        marginTop: "8px",
        marginBottom: "8px",
        height: "calc(100% - 16px)"
      }}
    >
      {expanded && (
        <div className="p-3 border-b border-slate-700/50">
          <h2 className="font-semibold text-slate-100 text-sm">Analysis Modules</h2>
          <p className="text-xs text-slate-300/80 mt-1">Select a module to begin</p>
        </div>
      )}
      
      <div className="overflow-y-auto flex-1 px-2 py-2">
        {modules.map((module) => (
          <ModulePanel 
            key={module.id}
            id={module.id}
            name={module.name}
            icon={module.icon}
            description={module.description}
            isActive={module.isActive}
            onToggle={() => onToggleModule(module.id)}
            expanded={expanded}
            onRunAnalysis={onRunAnalysis}
          />
        ))}
      </div>
      
      <div className="border-t border-slate-700/30 p-2">
        <button 
          onClick={onToggleExpanded}
          className="w-full flex items-center justify-center text-xs text-blue-300 hover:text-blue-100 py-1 transition-colors"
        >
          {expanded ? (
            <>
              <FontAwesomeIcon icon={faChevronLeft} className="mr-2" />
              <span>Collapse</span>
            </>
          ) : (
            <FontAwesomeIcon icon={faChevronRight} size="xs" />
          )}
        </button>
      </div>
    </aside>
  );
}
