import { useState, useEffect } from 'react';
import { api } from '../services/api';
import { User } from '../types/auth.types';

export const useAuth = () => {
    const [user, setUser] = useState<User | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchUser = async () => {
            try {
                const response = await api.get('/auth/me');
                setUser(response.data);
            } catch (err) {
                setError('Failed to fetch user data');
            } finally {
                setLoading(false);
            }
        };

        fetchUser();
    }, []);

    const login = async (email: string, password: string) => {
        try {
            const response = await api.post('/auth/login', { email, password });
            setUser(response.data);
        } catch (err) {
            setError('Login failed');
        }
    };

    const register = async (email: string, password: string) => {
        try {
            const response = await api.post('/auth/register', { email, password });
            setUser(response.data);
        } catch (err) {
            setError('Registration failed');
        }
    };

    const logout = async () => {
        try {
            await api.post('/auth/logout');
            setUser(null);
        } catch (err) {
            setError('Logout failed');
        }
    };

    return {
        user,
        loading,
        error,
        login,
        register,
        logout,
    };
};