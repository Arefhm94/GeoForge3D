export interface Rectangle {
  northEast: {
    lat: number;
    lng: number;
  };
  southWest: {
    lat: number;
    lng: number;
  };
}

export interface GeoJSONFeature {
  type: string;
  properties: {
    [key: string]: any;
  };
  geometry: {
    type: string;
    coordinates: number[][][];
  };
}

export interface GeoJSON {
  type: string;
  features: GeoJSONFeature[];
}

export interface BuildingFootprint {
  id: string;
  area: number;
  geoJson: GeoJSON;
}