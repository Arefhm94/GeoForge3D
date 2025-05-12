import React, { useState } from 'react';
import { MapContainer, TileLayer, Rectangle } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import LayerSelector from './LayerSelector';
import SearchBar from './SearchBar';
import RectangleDrawer from './RectangleDrawer';

const MapComponent = () => {
    const [rectangleBounds, setRectangleBounds] = useState(null);

    const handleRectangleDrawn = (bounds) => {
        setRectangleBounds(bounds);
    };

    return (
        <div>
            <SearchBar />
            <LayerSelector />
            <MapContainer center={[51.505, -0.09]} zoom={13} style={{ height: '100vh', width: '100%' }}>
                <TileLayer
                    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                    attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                />
                {rectangleBounds && <Rectangle bounds={rectangleBounds} />}
                <RectangleDrawer onRectangleDrawn={handleRectangleDrawn} />
            </MapContainer>
        </div>
    );
};

export default MapComponent;