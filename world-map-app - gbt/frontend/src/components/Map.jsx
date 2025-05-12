import React, { useState, useEffect } from 'react';
import { MapContainer, TileLayer, Rectangle, useMap } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';

const Map = () => {
    const [rectangleBounds, setRectangleBounds] = useState(null);
    const [geoJson, setGeoJson] = useState(null);
    const [layer, setLayer] = useState('streets');

    const handleMapClick = (event) => {
        const bounds = [[event.latlng.lat - 0.01, event.latlng.lng - 0.01], [event.latlng.lat + 0.01, event.latlng.lng + 0.01]];
        setRectangleBounds(bounds);
    };

    const exportGeoJson = () => {
        if (rectangleBounds) {
            const geoJsonData = {
                type: "FeatureCollection",
                features: [{
                    type: "Feature",
                    geometry: {
                        type: "Polygon",
                        coordinates: [[
                            [rectangleBounds[0][1], rectangleBounds[0][0]],
                            [rectangleBounds[0][1], rectangleBounds[1][0]],
                            [rectangleBounds[1][1], rectangleBounds[1][0]],
                            [rectangleBounds[1][1], rectangleBounds[0][0]],
                            [rectangleBounds[0][1], rectangleBounds[0][0]]
                        ]]
                    },
                    properties: {}
                }]
            };
            setGeoJson(geoJsonData);
            // Here you would typically send the geoJsonData to the backend
        }
    };

    useEffect(() => {
        if (geoJson) {
            // Logic to handle the geoJson data, e.g., download or send to backend
        }
    }, [geoJson]);

    return (
        <div>
            <MapContainer center={[20, 0]} zoom={2} style={{ height: '600px', width: '100%' }} onClick={handleMapClick}>
                <TileLayer
                    url={`https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png`}
                    attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                />
                {rectangleBounds && <Rectangle bounds={rectangleBounds} color="blue" />}
            </MapContainer>
            <button onClick={exportGeoJson}>Export GeoJSON</button>
        </div>
    );
};

export default Map;