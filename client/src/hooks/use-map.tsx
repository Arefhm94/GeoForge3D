import { useRef, MutableRefObject } from "react";
import L from "leaflet";

export default function useMap() {
  const mapRef = useRef<L.Map | null>(null);
  
  return {
    mapRef: mapRef as MutableRefObject<L.Map>,
  };
}
