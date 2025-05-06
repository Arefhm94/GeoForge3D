// Type definitions for leaflet-draw
import * as L from 'leaflet';

declare module 'leaflet' {
  // Extend Map interface for leaflet-draw
  interface Map {
    drawControl?: Control.Draw;
  }
  
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
    
    class Rectangle {
      constructor(map: L.Map, options?: any);
      enable(): void;
      disable(): void;
    }
    
    class Polygon {
      constructor(map: L.Map, options?: any);
      enable(): void;
      disable(): void;
    }
    
    class Marker {
      constructor(map: L.Map, options?: any);
      enable(): void;
      disable(): void;
    }
  }
  
  namespace Control {
    class Draw extends L.Control {
      constructor(options?: Draw.IDrawControlOptions);
      options: any;
    }
  }
  
  namespace EditToolbar {
    class Edit {
      constructor(map: L.Map, options?: any);
      enable(): void;
      disable(): void;
    }
    
    class Delete {
      constructor(map: L.Map, options?: any);
      enable(): void;
      disable(): void;
    }
  }
}

declare module 'leaflet-draw' {
  export = L.Draw;
}