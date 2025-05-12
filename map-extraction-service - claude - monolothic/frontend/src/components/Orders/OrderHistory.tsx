import React, { useEffect, useState } from 'react';
import { fetchOrderHistory } from '../../services/order.service';
import { Order } from '../../types/order.types';

const OrderHistory: React.FC = () => {
    const [orders, setOrders] = useState<Order[]>([]);
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const getOrderHistory = async () => {
            try {
                const orderData = await fetchOrderHistory();
                setOrders(orderData);
            } catch (err) {
                setError('Failed to fetch order history');
            } finally {
                setLoading(false);
            }
        };

        getOrderHistory();
    }, []);

    if (loading) {
        return <div>Loading...</div>;
    }

    if (error) {
        return <div>{error}</div>;
    }

    return (
        <div>
            <h2>Your Order History</h2>
            <ul>
                {orders.map(order => (
                    <li key={order.id}>
                        <div>Order ID: {order.id}</div>
                        <div>Area: {order.area} m²</div>
                        <div>Price: ${order.price}</div>
                        <div>Date: {new Date(order.date).toLocaleDateString()}</div>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default OrderHistory;