import React, { useState } from 'react';

const PricingCalculator: React.FC = () => {
    const [area, setArea] = useState<number>(0);
    const [price, setPrice] = useState<number>(0);

    const calculatePrice = (area: number) => {
        const freeArea = 1000000; // 1 km² in square meters
        const costPerSquareMeter = 2; // $2 per square meter

        if (area <= freeArea) {
            return 0; // Free for the first 1 km²
        } else {
            return (area - freeArea) * costPerSquareMeter;
        }
    };

    const handleAreaChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        const newArea = parseFloat(event.target.value);
        setArea(newArea);
        setPrice(calculatePrice(newArea));
    };

    return (
        <div>
            <h2>Pricing Calculator</h2>
            <input
                type="number"
                value={area}
                onChange={handleAreaChange}
                placeholder="Enter area in square meters"
            />
            <h3>Total Price: ${price.toFixed(2)}</h3>
        </div>
    );
};

export default PricingCalculator;