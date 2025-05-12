import React from 'react';
import { useEffect, useState } from 'react';
import { getUserOrders } from '../services/api';
import OrderList from '../components/OrderList';

const Dashboard = () => {
    const [orders, setOrders] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchOrders = async () => {
            const userOrders = await getUserOrders();
            setOrders(userOrders);
            setLoading(false);
        };

        fetchOrders();
    }, []);

    if (loading) {
        return <div>Loading...</div>;
    }

    return (
        <div>
            <h1>Dashboard</h1>
            <h2>Your Orders</h2>
            <OrderList orders={orders} />
        </div>
    );
};

export default Dashboard;