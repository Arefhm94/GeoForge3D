import React, { useState } from 'react';
import { MapContainer, Rectangle, TileLayer } from 'react-leaflet';

const RectangleDrawer = () => {
    const [bounds, setBounds] = useState(null);
    const [rectangle, setRectangle] = useState(null);

    const handleMapClick = (event) => {
        if (!bounds) {
            setBounds([event.latlng, event.latlng]);
        } else {
            setBounds([bounds[0], event.latlng]);
            setRectangle([bounds[0], event.latlng]);
        }
    };

    const handleExportGeoJSON = () => {
        if (rectangle) {
            const geoJson = {
                type: "Feature",
                geometry: {
                    type: "Polygon",
                    coordinates: [
                        [
                            [rectangle[0].lng, rectangle[0].lat],
                            [rectangle[1].lng, rectangle[0].lat],
                            [rectangle[1].lng, rectangle[1].lat],
                            [rectangle[0].lng, rectangle[1].lat],
                            [rectangle[0].lng, rectangle[0].lat]
                        ]
                    ]
                },
                properties: {}
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
            <MapContainer center={[51.505, -0.09]} zoom={13} style={{ height: "500px", width: "100%" }} onClick={handleMapClick}>
                <TileLayer
                    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                    attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                />
                {bounds && (
                    <Rectangle bounds={bounds} color="blue" />
                )}
            </MapContainer>
            <button onClick={handleExportGeoJSON} disabled={!rectangle}>Export GeoJSON</button>
        </div>
    );
};

export default RectangleDrawer;