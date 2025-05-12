import React, { useEffect, useRef } from 'react';
import { MapContainer, TileLayer, Rectangle } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import LayerSelector from './LayerSelector';
import SearchBar from './SearchBar';
import DrawTools from './DrawTools';

const Map = () => {
    const mapRef = useRef();

    useEffect(() => {
        // Initialize map and set view
        const map = mapRef.current;
        if (map) {
            map.setView([20, 0], 2); // Center the map on the world
        }
    }, []);

    const handleRectangleDraw = (bounds) => {
        // Logic to handle rectangle drawing
        console.log('Rectangle bounds:', bounds);
        // Call function to export GeoJSON here
    };

    return (
        <div>
            <SearchBar />
            <LayerSelector />
            <DrawTools onDraw={handleRectangleDraw} />
            <MapContainer ref={mapRef} style={{ height: '100vh', width: '100%' }}>
                <TileLayer
                    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                    attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                />
                {/* Add rectangle layer here based on user input */}
            </MapContainer>
        </div>
    );
};

export default Map;