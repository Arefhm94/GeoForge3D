import api from './api';
import { Order } from '../types/order.types';

const orderService = {
    createOrder: async (rectangle: { coordinates: number[][]; }, userId: string): Promise<Order> => {
        const response = await api.post('/orders', { rectangle, userId });
        return response.data;
    },

    getOrderHistory: async (userId: string): Promise<Order[]> => {
        const response = await api.get(`/orders/history/${userId}`);
        return response.data;
    },

    checkoutOrder: async (orderId: string): Promise<void> => {
        await api.post(`/orders/checkout/${orderId}`);
    },

    calculatePricing: async (area: number): Promise<number> => {
        const response = await api.get(`/orders/pricing/${area}`);
        return response.data;
    }
};

export default orderService;