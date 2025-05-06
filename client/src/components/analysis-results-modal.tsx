import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faTimes, faDownload } from "@fortawesome/free-solid-svg-icons";
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";

interface AnalysisResultsModalProps {
  onClose: () => void;
  area: number;
}

export default function AnalysisResultsModal({ onClose, area }: AnalysisResultsModalProps) {
  // This would normally come from an API response
  const analysisData = {
    landCover: [
      { label: "Forest", percentage: 42, color: "bg-green-600" },
      { label: "Urban/Built-up", percentage: 28, color: "bg-gray-600" },
      { label: "Water", percentage: 15, color: "bg-blue-600" },
      { label: "Agriculture", percentage: 12, color: "bg-yellow-600" },
      { label: "Other", percentage: 3, color: "bg-orange-500" }
    ],
    summary: [
      `The selected area (${area} m²) is primarily covered by forest (42%) and urban development (28%).`,
      "Water bodies make up 15% of the area, suggesting potential biodiversity hotspots.",
      "Agricultural land covers 12%, which is below the regional average of 23%.",
      "The urban/forest interface presents potential wildfire risk zones in the northern section."
    ]
  };
  
  return (
    <Dialog open={true} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-3xl">
        <DialogHeader>
          <DialogTitle>Land Cover Analysis Results</DialogTitle>
          <button 
            onClick={onClose} 
            className="absolute right-4 top-4 text-gray-400 hover:text-gray-600"
          >
            <FontAwesomeIcon icon={faTimes} className="text-xl" />
          </button>
        </DialogHeader>
        
        <div className="p-4">
          <div className="flex flex-col md:flex-row gap-6">
            <div className="flex-1">
              <h4 className="font-medium text-gray-700 mb-3">Land Cover Composition</h4>
              <div className="rounded-md border border-gray-200 p-4 bg-gray-50">
                {analysisData.landCover.map((item, index) => (
                  <div key={index} className="mb-3 last:mb-0">
                    <div className="flex justify-between mb-1">
                      <span className="text-sm text-gray-600">{item.label}</span>
                      <span className="text-sm font-medium">{item.percentage}%</span>
                    </div>
                    <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
                      <div 
                        className={`h-full ${item.color} rounded-full`} 
                        style={{ width: `${item.percentage}%` }}
                      ></div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
            
            <div className="flex-1">
              <h4 className="font-medium text-gray-700 mb-3">Analysis Summary</h4>
              <div className="rounded-md border border-gray-200 p-4 bg-gray-50 text-sm text-gray-700 space-y-3">
                {analysisData.summary.map((paragraph, index) => (
                  <p key={index}>{paragraph}</p>
                ))}
              </div>
              <div className="mt-4">
                <Button className="w-full bg-primary hover:bg-blue-600 flex items-center justify-center gap-2">
                  <FontAwesomeIcon icon={faDownload} />
                  Download Full Report (PDF)
                </Button>
              </div>
            </div>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
}
