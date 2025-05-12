import React, { useState } from 'react';
import { useHistory } from 'react-router-dom';
import { processPayment } from '../../services/api';

const Checkout = () => {
    const [amount, setAmount] = useState(0);
    const [error, setError] = useState('');
    const history = useHistory();

    const handlePayment = async () => {
        try {
            const response = await processPayment(amount);
            if (response.success) {
                history.push('/success');
            } else {
                setError(response.message);
            }
        } catch (err) {
            setError('Payment processing failed. Please try again.');
        }
    };

    return (
        <div className="checkout">
            <h2>Checkout</h2>
            <div>
                <label>Total Amount: </label>
                <input
                    type="number"
                    value={amount}
                    onChange={(e) => setAmount(e.target.value)}
                    placeholder="Enter amount"
                />
            </div>
            {error && <p className="error">{error}</p>}
            <button onClick={handlePayment}>Pay Now</button>
        </div>
    );
};

export default Checkout;