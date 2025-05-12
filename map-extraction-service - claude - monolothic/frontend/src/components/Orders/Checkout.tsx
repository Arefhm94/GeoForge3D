import React, { useState } from 'react';
import { useHistory } from 'react-router-dom';
import { createOrder } from '../../services/order.service';
import { useAuth } from '../../hooks/useAuth';

const Checkout: React.FC = () => {
    const [area, setArea] = useState<number>(0);
    const [totalCost, setTotalCost] = useState<number>(0);
    const { user } = useAuth();
    const history = useHistory();

    const handleAreaChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const newArea = parseFloat(e.target.value);
        setArea(newArea);
        calculateCost(newArea);
    };

    const calculateCost = (area: number) => {
        const freeArea = 1000000; // 1 km² in square meters
        const costPerSquareMeter = 2;
        let cost = 0;

        if (area > freeArea) {
            cost = (area - freeArea) * costPerSquareMeter;
        }

        setTotalCost(cost);
    };

    const handleCheckout = async () => {
        if (!user) {
            alert('You need to be logged in to proceed with the checkout.');
            return;
        }

        try {
            await createOrder({ area, totalCost });
            alert('Order created successfully!');
            history.push('/orders');
        } catch (error) {
            console.error('Error creating order:', error);
            alert('Failed to create order. Please try again.');
        }
    };

    return (
        <div>
            <h2>Checkout</h2>
            <label>
                Area (m²):
                <input type="number" value={area} onChange={handleAreaChange} />
            </label>
            <p>Total Cost: ${totalCost}</p>
            <button onClick={handleCheckout}>Proceed to Payment</button>
        </div>
    );
};

export default Checkout;