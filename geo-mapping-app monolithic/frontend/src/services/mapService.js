import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000/api'; // Adjust the base URL as needed

export const fetchMapData = async () => {
    try {
        const response = await axios.get(`${API_BASE_URL}/map_data`);
        return response.data;
    } catch (error) {
        console.error('Error fetching map data:', error);
        throw error;
    }
};

export const exportGeoJSON = async (rectangle) => {
    try {
        const response = await axios.post(`${API_BASE_URL}/map_data/export`, rectangle, {
            responseType: 'blob', // Expecting a GeoJSON file
        });
        return response.data;
    } catch (error) {
        console.error('Error exporting GeoJSON:', error);
        throw error;
    }
};

export const extractBuildingFootprints = async (rectangle) => {
    try {
        const response = await axios.post(`${API_BASE_URL}/buildings/extract`, rectangle);
        return response.data;
    } catch (error) {
        console.error('Error extracting building footprints:', error);
        throw error;
    }
};