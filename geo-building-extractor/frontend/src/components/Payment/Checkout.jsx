import React, { useState } from 'react';
import { useHistory } from 'react-router-dom';
import { processPayment } from '../../services/api';
import PricingCalculator from './PricingCalculator';

const Checkout = () => {
    const [area, setArea] = useState(0);
    const [paymentStatus, setPaymentStatus] = useState(null);
    const history = useHistory();

    const handlePayment = async () => {
        try {
            const response = await processPayment(area);
            if (response.success) {
                setPaymentStatus('Payment successful!');
                // Redirect or perform further actions
                history.push('/success');
            } else {
                setPaymentStatus('Payment failed. Please try again.');
            }
        } catch (error) {
            setPaymentStatus('An error occurred. Please try again later.');
        }
    };

    return (
        <div className="checkout-container">
            <h2>Checkout</h2>
            <PricingCalculator setArea={setArea} />
            <button onClick={handlePayment}>Pay Now</button>
            {paymentStatus && <p>{paymentStatus}</p>}
        </div>
    );
};

export default Checkout;