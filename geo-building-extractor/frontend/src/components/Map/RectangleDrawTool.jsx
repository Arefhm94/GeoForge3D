import React, { useState } from 'react';
import { MapContainer, TileLayer, Rectangle } from 'react-leaflet';

const RectangleDrawTool = () => {
    const [bounds, setBounds] = useState(null);

    const handleMapClick = (event) => {
        if (!bounds) {
            setBounds([[event.latlng.lat, event.latlng.lng]]);
        } else {
            const newBounds = [...bounds, [event.latlng.lat, event.latlng.lng]];
            setBounds(newBounds);
        }
    };

    const handleExportGeoJSON = () => {
        if (bounds) {
            const geoJson = {
                type: "FeatureCollection",
                features: [
                    {
                        type: "Feature",
                        geometry: {
                            type: "Polygon",
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
            const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(geoJson));
            const downloadAnchorNode = document.createElement('a');
            downloadAnchorNode.setAttribute("href", dataStr);
            downloadAnchorNode.setAttribute("download", "rectangle.geojson");
            document.body.appendChild(downloadAnchorNode);
            downloadAnchorNode.click();
            downloadAnchorNode.remove();
        }
    };

    return (
        <div>
            <MapContainer center={[51.505, -0.09]} zoom={13} onClick={handleMapClick} style={{ height: "500px", width: "100%" }}>
                <TileLayer
                    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                    attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                />
                {bounds && <Rectangle bounds={bounds} />}
            </MapContainer>
            <button onClick={handleExportGeoJSON} disabled={!bounds}>Export GeoJSON</button>
        </div>
    );
};

export default RectangleDrawTool;