import React, { useEffect, useState } from 'react';
import { fetchOrders } from '../services/api';

const Orders = () => {
    const [orders, setOrders] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const getOrders = async () => {
            try {
                const response = await fetchOrders();
                setOrders(response.data);
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };

        getOrders();
    }, []);

    if (loading) {
        return <div>Loading...</div>;
    }

    if (error) {
        return <div>Error: {error}</div>;
    }

    return (
        <div>
            <h1>Your Orders</h1>
            <ul>
                {orders.map(order => (
                    <li key={order.id}>
                        <p>Order ID: {order.id}</p>
                        <p>Area: {order.area} m²</p>
                        <p>Cost: ${order.cost}</p>
                        <p>Status: {order.status}</p>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default Orders;