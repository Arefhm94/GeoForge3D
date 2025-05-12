import { useEffect, useRef, useState } from 'react';
import { Map, View } from 'ol';
import 'ol/ol.css';
import { fromLonLat } from 'ol/proj';
import { Draw } from 'ol/interaction';
import { Vector as VectorLayer } from 'ol/layer';
import { Vector as VectorSource } from 'ol/source';
import { Feature } from 'ol';
import { GeometryType } from 'ol/geom';

const useMap = () => {
    const mapRef = useRef<HTMLDivElement | null>(null);
    const [map, setMap] = useState<Map | null>(null);
    const [drawInteraction, setDrawInteraction] = useState<Draw | null>(null);
    const [rectangle, setRectangle] = useState<Feature | null>(null);
    const vectorSource = new VectorSource();
    const vectorLayer = new VectorLayer({
        source: vectorSource,
    });

    useEffect(() => {
        if (mapRef.current) {
            const initialMap = new Map({
                target: mapRef.current,
                layers: [
                    // Add your base layer here
                    vectorLayer,
                ],
                view: new View({
                    center: fromLonLat([0, 0]), // Set initial center
                    zoom: 2, // Set initial zoom level
                }),
            });
            setMap(initialMap);
        }
    }, [mapRef]);

    const startDrawingRectangle = () => {
        if (map) {
            const draw = new Draw({
                source: vectorSource,
                type: GeometryType.Polygon,
            });
            draw.on('drawend', (event) => {
                setRectangle(event.feature);
                map.removeInteraction(draw);
            });
            map.addInteraction(draw);
            setDrawInteraction(draw);
        }
    };

    const exportGeoJSON = () => {
        if (rectangle) {
            const geoJSON = new GeoJSON().writeFeature(rectangle);
            return geoJSON;
        }
        return null;
    };

    return {
        mapRef,
        startDrawingRectangle,
        exportGeoJSON,
    };
};

export default useMap;