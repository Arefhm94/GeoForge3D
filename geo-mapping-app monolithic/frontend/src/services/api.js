import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000/api'; // Adjust the base URL as needed

export const registerUser = async (userData) => {
    const response = await axios.post(`${API_BASE_URL}/auth/register`, userData);
    return response.data;
};

export const loginUser = async (credentials) => {
    const response = await axios.post(`${API_BASE_URL}/auth/login`, credentials);
    return response.data;
};

export const fetchMapData = async (params) => {
    const response = await axios.get(`${API_BASE_URL}/map_data`, { params });
    return response.data;
};

export const extractBuildingFootprints = async (rectangle) => {
    const response = await axios.post(`${API_BASE_URL}/buildings/extract`, rectangle);
    return response.data;
};

export const processPayment = async (paymentData) => {
    const response = await axios.post(`${API_BASE_URL}/payments`, paymentData);
    return response.data;
};

export const downloadGeoJSON = async (orderId) => {
    const response = await axios.get(`${API_BASE_URL}/orders/${orderId}/download`, {
        responseType: 'blob',
    });
    return response.data;
};