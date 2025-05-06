import { LatLngBounds } from "leaflet";

/**
 * Calculate area in square meters from a LatLngBounds object
 * This uses the haversine formula to calculate distances between coordinates
 * 
 * @param bounds - The LatLngBounds object
 * @returns The area in square meters
 */
export function calculateArea(bounds: LatLngBounds): number {
  const southWest = bounds.getSouthWest();
  const northEast = bounds.getNorthEast();
  const northWest = { lat: northEast.lat, lng: southWest.lng };
  
  // Calculate width in meters
  const width = calculateHaversineDistance(
    southWest.lat,
    southWest.lng,
    northWest.lat,
    northWest.lng
  );
  
  // Calculate height in meters
  const height = calculateHaversineDistance(
    southWest.lat,
    southWest.lng,
    southWest.lat,
    northEast.lng
  );
  
  return Math.round(width * height);
}

/**
 * Calculate the haversine distance between two coordinates
 * 
 * @param lat1 - Latitude of the first coordinate in degrees
 * @param lon1 - Longitude of the first coordinate in degrees
 * @param lat2 - Latitude of the second coordinate in degrees
 * @param lon2 - Longitude of the second coordinate in degrees
 * @returns The distance in meters
 */
function calculateHaversineDistance(
  lat1: number,
  lon1: number,
  lat2: number,
  lon2: number
): number {
  const R = 6371000; // Earth radius in meters
  
  const dLat = degToRad(lat2 - lat1);
  const dLon = degToRad(lon2 - lon1);
  
  const a =
    Math.sin(dLat / 2) * Math.sin(dLat / 2) +
    Math.cos(degToRad(lat1)) * Math.cos(degToRad(lat2)) *
    Math.sin(dLon / 2) * Math.sin(dLon / 2);
  
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  const distance = R * c;
  
  return distance;
}

/**
 * Convert degrees to radians
 * 
 * @param degrees - The angle in degrees
 * @returns The angle in radians
 */
function degToRad(degrees: number): number {
  return degrees * (Math.PI / 180);
}
