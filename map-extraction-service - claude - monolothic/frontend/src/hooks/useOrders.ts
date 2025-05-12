import { useState, useEffect } from 'react';
import { getOrders, createOrder } from '../services/order.service';
import { Order } from '../types/order.types';

const useOrders = () => {
    const [orders, setOrders] = useState<Order[]>([]);
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchOrders = async () => {
            try {
                const fetchedOrders = await getOrders();
                setOrders(fetchedOrders);
            } catch (err) {
                setError('Failed to fetch orders');
            } finally {
                setLoading(false);
            }
        };

        fetchOrders();
    }, []);

    const addOrder = async (orderData: Omit<Order, 'id'>) => {
        try {
            const newOrder = await createOrder(orderData);
            setOrders((prevOrders) => [...prevOrders, newOrder]);
        } catch (err) {
            setError('Failed to create order');
        }
    };

    return { orders, loading, error, addOrder };
};

export default useOrders;