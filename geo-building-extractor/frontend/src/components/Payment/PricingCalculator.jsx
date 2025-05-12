import React, { useState } from 'react';

const PricingCalculator = ({ area }) => {
    const [cost, setCost] = useState(0);
    const freeArea = 1000000; // 1 km² in square meters
    const additionalCostPerSquareMeter = 2;

    const calculateCost = (area) => {
        if (area <= freeArea) {
            return 0;
        }
        const additionalArea = area - freeArea;
        return additionalArea * additionalCostPerSquareMeter;
    };

    React.useEffect(() => {
        const calculatedCost = calculateCost(area);
        setCost(calculatedCost);
    }, [area]);

    return (
        <div className="pricing-calculator">
            <h2>Pricing Calculator</h2>
            <p>Selected Area: {area} m²</p>
            <p>Total Cost: ${cost.toFixed(2)}</p>
        </div>
    );
};

export default PricingCalculator;