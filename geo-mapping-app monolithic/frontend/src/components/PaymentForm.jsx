import React, { useState } from 'react';
import axios from 'axios';

const PaymentForm = ({ userId, onPaymentSuccess }) => {
    const [amount, setAmount] = useState(0);
    const [error, setError] = useState(null);
    const [loading, setLoading] = useState(false);

    const handlePayment = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError(null);

        try {
            const response = await axios.post('/api/payments', {
                userId,
                amount,
            });

            if (response.data.success) {
                onPaymentSuccess(response.data);
            } else {
                setError(response.data.message);
            }
        } catch (err) {
            setError('Payment processing failed. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <form onSubmit={handlePayment}>
            <h2>Payment Form</h2>
            <div>
                <label htmlFor="amount">Amount (in $):</label>
                <input
                    type="number"
                    id="amount"
                    value={amount}
                    onChange={(e) => setAmount(e.target.value)}
                    required
                />
            </div>
            {error && <p style={{ color: 'red' }}>{error}</p>}
            <button type="submit" disabled={loading}>
                {loading ? 'Processing...' : 'Pay Now'}
            </button>
        </form>
    );
};

export default PaymentForm;