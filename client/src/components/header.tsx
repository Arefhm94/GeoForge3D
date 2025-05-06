import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faMapMarkedAlt, faQuestionCircle, faUser, faBars } from "@fortawesome/free-solid-svg-icons";

export default function Header() {
  return (
    <header className="bg-white shadow-sm">
      <div className="max-w-screen-xl mx-auto px-4 py-3 flex justify-between items-center">
        <div className="flex items-center space-x-3">
          <FontAwesomeIcon icon={faMapMarkedAlt} className="text-primary text-2xl" />
          <h1 className="text-xl font-semibold text-gray-800">GeoSpatial Analysis Tool</h1>
        </div>
        
        <div className="hidden md:flex items-center space-x-4">
          <button className="bg-gray-100 hover:bg-gray-200 text-gray-700 px-4 py-2 rounded-md text-sm flex items-center transition">
            <FontAwesomeIcon icon={faQuestionCircle} className="mr-2" />
            Help
          </button>
          <button className="bg-primary hover:bg-blue-600 text-white px-4 py-2 rounded-md text-sm flex items-center transition">
            <FontAwesomeIcon icon={faUser} className="mr-2" />
            Sign In
          </button>
        </div>
        
        <button className="md:hidden text-gray-700 text-2xl">
          <FontAwesomeIcon icon={faBars} />
        </button>
      </div>
    </header>
  );
}
