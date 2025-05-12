import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000'; // Adjust the base URL as needed

// Function to create a user account
export const createUser = async (userData) => {
    try {
        const response = await axios.post(`${API_BASE_URL}/auth/register`, userData);
        return response.data;
    } catch (error) {
        throw error.response.data;
    }
};

// Function to log in a user
export const loginUser = async (credentials) => {
    try {
        const response = await axios.post(`${API_BASE_URL}/auth/login`, credentials);
        return response.data;
    } catch (error) {
        throw error.response.data;
    }
};

// Function to get user profile
export const getUserProfile = async (token) => {
    try {
        const response = await axios.get(`${API_BASE_URL}/auth/profile`, {
            headers: { Authorization: `Bearer ${token}` },
        });
        return response.data;
    } catch (error) {
        throw error.response.data;
    }
};

// Function to create a rectangle and export GeoJSON
export const exportGeoJSON = async (rectangleData) => {
    try {
        const response = await axios.post(`${API_BASE_URL}/map/export-geojson`, rectangleData);
        return response.data;
    } catch (error) {
        throw error.response.data;
    }
};

// Function to extract building footprints
export const extractBuildingFootprints = async (rectangleData, token) => {
    try {
        const response = await axios.post(`${API_BASE_URL}/extraction/buildings`, rectangleData, {
            headers: { Authorization: `Bearer ${token}` },
        });
        return response.data;
    } catch (error) {
        throw error.response.data;
    }
};

// Function to process payment
export const processPayment = async (paymentData, token) => {
    try {
        const response = await axios.post(`${API_BASE_URL}/payment/checkout`, paymentData, {
            headers: { Authorization: `Bearer ${token}` },
        });
        return response.data;
    } catch (error) {
        throw error.response.data;
    }
};