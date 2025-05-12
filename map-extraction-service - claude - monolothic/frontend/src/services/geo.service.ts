import axios from 'axios';
import { GeoRectangle } from '../types/geo.types';

const API_BASE_URL = 'http://localhost:8000/api'; // Adjust the base URL as needed

export const createGeoRectangle = async (rectangle: GeoRectangle) => {
    const response = await axios.post(`${API_BASE_URL}/geo/rectangle`, rectangle);
    return response.data;
};

export const exportGeoJSON = async (rectangle: GeoRectangle) => {
    const response = await axios.post(`${API_BASE_URL}/geo/export`, rectangle, {
        responseType: 'blob', // To handle binary data
    });
    return response.data;
};

export const extractBuildingFootprints = async (rectangle: GeoRectangle) => {
    const response = await axios.post(`${API_BASE_URL}/geo/extract`, rectangle);
    return response.data;
};