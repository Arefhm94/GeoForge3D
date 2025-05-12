import React, { useEffect, useRef, useState } from 'react';
import { MapContainer, TileLayer, Rectangle, useMap } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import { fetchBuildings } from '../services/mapService';

const Map = () => {
    const [rectangleBounds, setRectangleBounds] = useState(null);
    const [buildings, setBuildings] = useState([]);
    const mapRef = useRef();

    const handleDrawRectangle = (e) => {
        const bounds = e.target.getBounds();
        setRectangleBounds(bounds);
        fetchBuildings(bounds).then(data => setBuildings(data));
    };

    const resetRectangle = () => {
        setRectangleBounds(null);
        setBuildings([]);
    };

    useEffect(() => {
        const map = mapRef.current;
        if (map) {
            map.on('draw:created', handleDrawRectangle);
        }
        return () => {
            if (map) {
                map.off('draw:created', handleDrawRectangle);
            }
        };
    }, []);

    return (
        <MapContainer center={[20, 0]} zoom={2} ref={mapRef} style={{ height: '100vh', width: '100%' }}>
            <TileLayer
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            />
            {rectangleBounds && (
                <Rectangle bounds={rectangleBounds} color="blue" />
            )}
            {/* Additional components like SearchBar and LayerSelector can be added here */}
        </MapContainer>
    );
};

export default Map;