import React, { useState, useEffect } from 'react';
import { MapContainer as LeafletMap, TileLayer, Rectangle } from 'react-leaflet';
import SearchBar from './SearchBar';
import LayerSelector from './LayerSelector';
import RectangleDrawTool from './RectangleDrawTool';
import 'leaflet/dist/leaflet.css';

const MapContainer = () => {
    const [bounds, setBounds] = useState(null);
    const [rectangle, setRectangle] = useState(null);

    const handleRectangleDraw = (rectangleBounds) => {
        setRectangle(rectangleBounds);
    };

    const handleExportGeoJSON = () => {
        if (rectangle) {
            const geoJson = {
                type: "FeatureCollection",
                features: [
                    {
                        type: "Feature",
                        geometry: {
                            type: "Polygon",
                            coordinates: [[
                                [rectangle.getWest(), rectangle.getSouth()],
                                [rectangle.getEast(), rectangle.getSouth()],
                                [rectangle.getEast(), rectangle.getNorth()],
                                [rectangle.getWest(), rectangle.getNorth()],
                                [rectangle.getWest(), rectangle.getSouth()]
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
            <SearchBar />
            <LayerSelector />
            <LeafletMap center={[51.505, -0.09]} zoom={13} style={{ height: "100vh", width: "100%" }}>
                <TileLayer
                    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                    attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                />
                {rectangle && <Rectangle bounds={rectangle.getBounds()} />}
                <RectangleDrawTool onDraw={handleRectangleDraw} />
            </LeafletMap>
            <button onClick={handleExportGeoJSON}>Export GeoJSON</button>
        </div>
    );
};

export default MapContainer;