import { useState } from 'react';

const useMapTools = () => {
    const [rectangle, setRectangle] = useState(null);
    const [layer, setLayer] = useState(null);
    const [searchQuery, setSearchQuery] = useState('');

    const createRectangle = (bounds) => {
        setRectangle(bounds);
    };

    const clearRectangle = () => {
        setRectangle(null);
    };

    const updateLayer = (newLayer) => {
        setLayer(newLayer);
    };

    const updateSearchQuery = (query) => {
        setSearchQuery(query);
    };

    return {
        rectangle,
        layer,
        searchQuery,
        createRectangle,
        clearRectangle,
        updateLayer,
        updateSearchQuery,
    };
};

export default useMapTools;