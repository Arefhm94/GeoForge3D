import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api'; // Adjust the base URL as needed

export const registerUser = async (userData) => {
    const response = await axios.post(`${API_BASE_URL}/auth/register`, userData);
    return response.data;
};

export const loginUser = async (credentials) => {
    const response = await axios.post(`${API_BASE_URL}/auth/login`, credentials);
    return response.data;
};

export const fetchUserProfile = async (token) => {
    const response = await axios.get(`${API_BASE_URL}/auth/profile`, {
        headers: { Authorization: `Bearer ${token}` },
    });
    return response.data;
};

export const createRectangle = async (rectangleData, token) => {
    const response = await axios.post(`${API_BASE_URL}/geo/rectangle`, rectangleData, {
        headers: { Authorization: `Bearer ${token}` },
    });
    return response.data;
};

export const exportGeoJSON = async (rectangleId, token) => {
    const response = await axios.get(`${API_BASE_URL}/geo/export/${rectangleId}`, {
        headers: { Authorization: `Bearer ${token}` },
    });
    return response.data;
};

export const fetchBuildingFootprints = async (rectangleId, token) => {
    const response = await axios.get(`${API_BASE_URL}/geo/footprints/${rectangleId}`, {
        headers: { Authorization: `Bearer ${token}` },
    });
    return response.data;
};

export const fetchOrderHistory = async (token) => {
    const response = await axios.get(`${API_BASE_URL}/orders/history`, {
        headers: { Authorization: `Bearer ${token}` },
    });
    return response.data;
};

export const checkoutOrder = async (orderData, token) => {
    const response = await axios.post(`${API_BASE_URL}/orders/checkout`, orderData, {
        headers: { Authorization: `Bearer ${token}` },
    });
    return response.data;
};