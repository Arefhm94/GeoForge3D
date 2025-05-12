import { useEffect, MutableRefObject } from "react";
import L from "leaflet";
import "leaflet-control-geocoder";

// Type definitions are maintained in client/src/types/leaflet-extensions.d.ts

interface UseLocationSearchProps {
  mapRef: MutableRefObject<L.Map | null>;
}

export default function useLocationSearch({ mapRef }: UseLocationSearchProps) {
  useEffect(() => {
    if (!mapRef.current) return;

    // Create a search control with a basic geocoder
    // Since the types are not fully compatible, we need to use 'any' here
    // for a production app, proper types would be defined
    const searchControl = new (L.Control as any).Geocoder({
      position: 'topleft',
      defaultMarkGeocode: false,
      placeholder: 'Search for a location...',
      collapsed: false,
      // @ts-ignore - Type issues with the geocoder library
      suggestMinLength: 3,
      // @ts-ignore - Type issues with the geocoder library
      suggestTimeout: 250,
      // @ts-ignore - Type issues with the geocoder library
      expand: 'click',
      // @ts-ignore - Type issues with the geocoder library
      showResultIcons: true
    }).on('markgeocode', function(e: any) {
      // Get the bounds of the search result
      const { center, name } = e.geocode;
      
      // Move to the location
      if (mapRef.current && center) {
        mapRef.current.setView(center, 14);
        
        // Add a marker at the location
        L.marker(center)
          .addTo(mapRef.current)
          .bindPopup(name || 'Selected location')
          .openPopup();
      }
    }).addTo(mapRef.current);

    return () => {
      if (mapRef.current) {
        mapRef.current.removeControl(searchControl);
      }
    };
  }, [mapRef]);

  return null;
}