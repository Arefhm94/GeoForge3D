import React, { useState } from 'react';
import { MapContainer, Rectangle, TileLayer } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';

const RectangleDrawer = () => {
    const [bounds, setBounds] = useState(null);
    const [rectangleVisible, setRectangleVisible] = useState(false);

    const handleMapClick = (event) => {
        if (!bounds) {
            setBounds([[event.latlng.lat, event.latlng.lng]]);
        } else {
            setBounds([...bounds, [event.latlng.lat, event.latlng.lng]]);
            setRectangleVisible(true);
        }
    };

    const handleExportGeoJSON = () => {
        if (bounds && bounds.length === 2) {
            const geoJson = {
                type: 'FeatureCollection',
                features: [
                    {
                        type: 'Feature',
                        geometry: {
                            type: 'Polygon',
                            coordinates: [[
                                [bounds[0][1], bounds[0][0]],
                                [bounds[1][1], bounds[0][0]],
                                [bounds[1][1], bounds[1][0]],
                                [bounds[0][1], bounds[1][0]],
                                [bounds[0][1], bounds[0][0]]
                            ]]
                        },
                        properties: {}
                    }
                ]
            };
            const dataStr = 'data:text/json;charset=utf-8,' + encodeURIComponent(JSON.stringify(geoJson));
            const downloadAnchorNode = document.createElement('a');
            downloadAnchorNode.setAttribute('href', dataStr);
            downloadAnchorNode.setAttribute('download', 'rectangle.geojson');
            document.body.appendChild(downloadAnchorNode);
            downloadAnchorNode.click();
            downloadAnchorNode.remove();
        }
    };

    return (
        <div>
            <MapContainer center={[51.505, -0.09]} zoom={13} style={{ height: '500px', width: '100%' }} onClick={handleMapClick}>
                <TileLayer
                    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                    attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                />
                {rectangleVisible && bounds && (
                    <Rectangle bounds={bounds} color="blue" />
                )}
            </MapContainer>
            <button onClick={handleExportGeoJSON} disabled={!rectangleVisible}>
                Export GeoJSON
            </button>
        </div>
    );
};

export default RectangleDrawer;