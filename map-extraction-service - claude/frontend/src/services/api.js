import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000'; // Adjust the base URL as needed

export const registerUser = async (userData) => {
    const response = await axios.post(`${API_BASE_URL}/auth/register`, userData);
    return response.data;
};

export const loginUser = async (credentials) => {
    const response = await axios.post(`${API_BASE_URL}/auth/login`, credentials);
    return response.data;
};

export const getUserProfile = async (token) => {
    const response = await axios.get(`${API_BASE_URL}/users/profile`, {
        headers: {
            Authorization: `Bearer ${token}`,
        },
    });
    return response.data;
};

export const searchLocation = async (query) => {
    const response = await axios.get(`${API_BASE_URL}/maps/search`, {
        params: { query },
    });
    return response.data;
};

export const createRectangle = async (rectangleData, token) => {
    const response = await axios.post(`${API_BASE_URL}/maps/rectangle`, rectangleData, {
        headers: {
            Authorization: `Bearer ${token}`,
        },
    });
    return response.data;
};

export const exportGeoJSON = async (rectangleId, token) => {
    const response = await axios.get(`${API_BASE_URL}/geojson/export/${rectangleId}`, {
        headers: {
            Authorization: `Bearer ${token}`,
        },
    });
    return response.data;
};

export const extractBuildingFootprint = async (rectangleId, token) => {
    const response = await axios.get(`${API_BASE_URL}/maps/buildings/${rectangleId}`, {
        headers: {
            Authorization: `Bearer ${token}`,
        },
    });
    return response.data;
};