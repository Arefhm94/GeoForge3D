import axios from 'axios';
import { AuthResponse, User } from '../types/auth.types';

const API_URL = 'http://localhost:8000/api/auth/';

const register = async (username: string, password: string): Promise<AuthResponse> => {
    const response = await axios.post(`${API_URL}register`, { username, password });
    return response.data;
};

const login = async (username: string, password: string): Promise<AuthResponse> => {
    const response = await axios.post(`${API_URL}login`, { username, password });
    return response.data;
};

const logout = async (): Promise<void> => {
    await axios.post(`${API_URL}logout`);
};

const getCurrentUser = (): User | null => {
    const user = localStorage.getItem('user');
    return user ? JSON.parse(user) : null;
};

const setUser = (user: User): void => {
    localStorage.setItem('user', JSON.stringify(user));
};

const clearUser = (): void => {
    localStorage.removeItem('user');
};

export default {
    register,
    login,
    logout,
    getCurrentUser,
    setUser,
    clearUser,
};