import React from 'react';

const LayerSelector = ({ layers, selectedLayer, onLayerChange }) => {
    return (
        <div className="layer-selector">
            <label htmlFor="layer-select">Select Layer:</label>
            <select
                id="layer-select"
                value={selectedLayer}
                onChange={(e) => onLayerChange(e.target.value)}
            >
                {layers.map((layer) => (
                    <option key={layer.id} value={layer.id}>
                        {layer.name}
                    </option>
                ))}
            </select>
        </div>
    );
};

export default LayerSelector;