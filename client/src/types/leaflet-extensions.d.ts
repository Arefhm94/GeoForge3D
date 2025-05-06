// Type definitions for Leaflet extensions
import * as L from 'leaflet';

declare module 'leaflet' {
  // Extend Map interface for control storage
  interface Map {
    drawControl?: Control.Draw;
  }

  // Define Draw namespace
  namespace Draw {
    interface IDrawControlOptions {
      position?: string;
      draw?: {
        polyline?: boolean | any;
        polygon?: boolean | any;
        rectangle?: boolean | any;
        circle?: boolean | any;
        marker?: boolean | any;
        circlemarker?: boolean | any;
      };
      edit?: {
        featureGroup: FeatureGroup;
        remove?: boolean;
      };
    }

    class Event {
      static CREATED: string;
      static EDITED: string;
      static DELETED: string;
      static DRAWSTART: string;
      static DRAWSTOP: string;
      static EDITSTART: string;
      static EDITSTOP: string;
      static DELETESTART: string;
      static DELETESTOP: string;
    }
  }

  // Define Control namespace extensions
  namespace Control {
    class Draw extends L.Control {
      constructor(options?: Draw.IDrawControlOptions);
    }

    class Geocoder extends L.Control {
      constructor(options?: any);
    }
  }

  // Define ESRI namespace
  namespace esri {
    function basemapLayer(id: string, options?: any): TileLayer;
  }
}

// Define types for leaflet-control-geocoder
declare module 'leaflet-control-geocoder' {
  export = L.Control.Geocoder;
}

// Define types for leaflet-draw
declare module 'leaflet-draw' {
  export = L.Draw;
}

// Define types for esri-leaflet
declare module 'esri-leaflet' {
  export = L.esri;
}