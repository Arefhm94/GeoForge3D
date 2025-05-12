import React from 'react';

const PricingInfo = () => {
    return (
        <div className="pricing-info">
            <h2>Pricing Information</h2>
            <p>Welcome to our map extraction service! Here are the details regarding our pricing:</p>
            <ul>
                <li>First 1 km² of data extraction: <strong>Free</strong></li>
                <li>After the first 1 km²: <strong>$2 per square meter</strong></li>
            </ul>
            <p>For any questions or further information, please contact our support team.</p>
        </div>
    );
};

export default PricingInfo;