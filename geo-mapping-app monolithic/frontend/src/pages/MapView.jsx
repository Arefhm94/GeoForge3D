import React, { useState, useEffect } from 'react';
import Map from '../components/Map';
import SearchBar from '../components/SearchBar';
import LayerSelector from '../components/LayerSelector';
import RectangleDrawer from '../components/RectangleDrawer';
import { fetchGeoJson, extractBuildingFootprints } from '../services/mapService';

const MapView = () => {
    const [rectangle, setRectangle] = useState(null);
    const [geoJson, setGeoJson] = useState(null);
    const [buildingFootprints, setBuildingFootprints] = useState([]);

    const handleRectangleDrawn = (rect) => {
        setRectangle(rect);
    };

    const handleExportGeoJson = async () => {
        if (rectangle) {
            const geoJsonData = await fetchGeoJson(rectangle);
            setGeoJson(geoJsonData);
        }
    };

    const handleExtractBuildings = async () => {
        if (rectangle) {
            const footprints = await extractBuildingFootprints(rectangle);
            setBuildingFootprints(footprints);
        }
    };

    useEffect(() => {
        // Any additional setup or data fetching can be done here
    }, []);

    return (
        <div>
            <h1>Map View</h1>
            <SearchBar />
            <LayerSelector />
            <RectangleDrawer onRectangleDrawn={handleRectangleDrawn} />
            <Map rectangle={rectangle} />
            <button onClick={handleExportGeoJson}>Export GeoJSON</button>
            <button onClick={handleExtractBuildings}>Extract Building Footprints</button>
            {geoJson && <pre>{JSON.stringify(geoJson, null, 2)}</pre>}
            {buildingFootprints.length > 0 && (
                <div>
                    <h2>Building Footprints</h2>
                    <pre>{JSON.stringify(buildingFootprints, null, 2)}</pre>
                </div>
            )}
        </div>
    );
};

export default MapView;