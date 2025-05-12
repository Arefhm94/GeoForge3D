import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000'; // Adjust the base URL as needed

export const fetchMapLayers = async () => {
    try {
        const response = await axios.get(`${API_BASE_URL}/maps/layers`);
        return response.data;
    } catch (error) {
        console.error('Error fetching map layers:', error);
        throw error;
    }
};

export const extractGeoJson = async (rectangle) => {
    try {
        const response = await axios.post(`${API_BASE_URL}/geojson/extract`, rectangle);
        return response.data;
    } catch (error) {
        console.error('Error extracting GeoJSON:', error);
        throw error;
    }
};

export const fetchBuildingFootprints = async (rectangle) => {
    try {
        const response = await axios.post(`${API_BASE_URL}/maps/buildings`, rectangle);
        return response.data;
    } catch (error) {
        console.error('Error fetching building footprints:', error);
        throw error;
    }
};