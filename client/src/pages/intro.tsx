import React from 'react';
import { Link } from 'wouter';
import EarthBackground from '../components/earth-background';

export default function IntroPage() {
  return (
    <div className="min-h-screen flex items-center justify-center relative overflow-hidden">
      <EarthBackground />
      
      <div className="text-center z-10">
        <h1 className="text-5xl font-bold mb-6 text-white">
          GeoSpatial
        </h1>
        
        <p className="text-xl text-slate-200 mb-10 max-w-md mx-auto">
          Interactive map visualization tool
        </p>
        
        <Link href="/map" className="inline-flex items-center justify-center rounded-full bg-blue-600 px-8 py-3 text-white font-medium text-lg shadow-lg hover:bg-blue-700 transition-all duration-300">
          Try Me
        </Link>
      </div>
    </div>
  );
}