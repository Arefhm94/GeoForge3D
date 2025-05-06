import React from 'react';
import { Link } from 'wouter';

export default function IntroPage() {
  return (
    <div className="bg-slate-900 min-h-screen flex flex-col items-center justify-center text-white py-10 px-4">
      <div className="max-w-4xl w-full bg-slate-800/30 backdrop-blur-md rounded-xl shadow-xl p-8 relative overflow-hidden border border-slate-700/50">
        <div className="absolute inset-0 bg-gradient-to-br from-blue-600/20 to-purple-600/20 z-0"></div>
        
        <div className="relative z-10">
          <div className="absolute top-4 right-4">
            <Link href="/map" className="inline-flex items-center justify-center rounded-md bg-gradient-to-r from-blue-500 to-indigo-600 px-5 py-2.5 text-white font-medium shadow-lg hover:shadow-xl hover:-translate-y-1 transition-all duration-300 hover:from-blue-600 hover:to-indigo-700">
              Try Me
            </Link>
          </div>
          
          <h1 className="text-4xl md:text-5xl font-bold mb-6 bg-gradient-to-r from-blue-400 to-indigo-500 bg-clip-text text-transparent">
            GeoSpatial Analysis Platform
          </h1>
          
          <p className="text-lg text-slate-300 mb-8 max-w-3xl">
            An advanced geospatial web application for interactive map visualization, offering powerful drawing, measurement, and geographic exploration tools.
          </p>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
            <div className="bg-slate-800/50 backdrop-blur-md p-6 rounded-lg border border-slate-700/50 hover:border-blue-500/50 transition-all shadow-lg hover:shadow-blue-900/20 hover:-translate-y-1">
              <div className="text-blue-400 text-xl font-semibold mb-3">Map Visualization</div>
              <p className="text-slate-300">
                Explore different map styles including Dark, Light, Satellite with Labels, and Topographic views with an intuitive layer selection interface.
              </p>
            </div>
            
            <div className="bg-slate-800/50 backdrop-blur-md p-6 rounded-lg border border-slate-700/50 hover:border-blue-500/50 transition-all shadow-lg hover:shadow-blue-900/20 hover:-translate-y-1">
              <div className="text-blue-400 text-xl font-semibold mb-3">Area Selection & Measurement</div>
              <p className="text-slate-300">
                Draw rectangles to precisely select areas with automatic area calculation in square meters, with detailed coordinate display.
              </p>
            </div>
            
            <div className="bg-slate-800/50 backdrop-blur-md p-6 rounded-lg border border-slate-700/50 hover:border-blue-500/50 transition-all shadow-lg hover:shadow-blue-900/20 hover:-translate-y-1">
              <div className="text-blue-400 text-xl font-semibold mb-3">GeoJSON Import/Export</div>
              <p className="text-slate-300">
                Import your GeoJSON files via drag-and-drop or export your selected areas as GeoJSON for use in other applications.
              </p>
            </div>
            
            <div className="bg-slate-800/50 backdrop-blur-md p-6 rounded-lg border border-slate-700/50 hover:border-blue-500/50 transition-all shadow-lg hover:shadow-blue-900/20 hover:-translate-y-1">
              <div className="text-blue-400 text-xl font-semibold mb-3">Advanced Analysis Modules</div>
              <p className="text-slate-300">
                Leverage powerful modules for buildings detection, terrain analysis, green areas extraction, and more with our specialized tools.
              </p>
            </div>
          </div>
          
          <div className="text-center mt-10">
            <Link href="/map" className="inline-flex items-center justify-center rounded-md bg-gradient-to-r from-blue-500 to-indigo-600 px-8 py-3 text-white font-medium text-lg shadow-lg hover:shadow-xl hover:-translate-y-1 transition-all duration-300 hover:from-blue-600 hover:to-indigo-700">
              Start Exploring
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}