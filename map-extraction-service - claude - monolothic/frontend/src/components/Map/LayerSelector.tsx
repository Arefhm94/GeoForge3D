import React from 'react';

const LayerSelector = () => {
    const layers = [
        { id: 'satellite', name: 'Satellite' },
        { id: 'streets', name: 'Streets' },
        { id: 'terrain', name: 'Terrain' },
    ];

    const handleLayerChange = (event) => {
        const selectedLayer = event.target.value;
        // Logic to change the map layer goes here
        console.log(`Selected layer: ${selectedLayer}`);
    };

    return (
        <div className="layer-selector">
            <label htmlFor="layer-select">Select Map Layer:</label>
            <select id="layer-select" onChange={handleLayerChange}>
                {layers.map(layer => (
                    <option key={layer.id} value={layer.id}>
                        {layer.name}
                    </option>
                ))}
            </select>
        </div>
    );
};

export default LayerSelector;