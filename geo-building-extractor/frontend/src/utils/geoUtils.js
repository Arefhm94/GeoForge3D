// This file provides utility functions for geographic calculations.

export const calculateArea = (rectangle) => {
    const { northEast, southWest } = rectangle;
    const width = northEast.lng - southWest.lng;
    const height = northEast.lat - southWest.lat;
    return Math.abs(width * height);
};

export const rectangleToGeoJSON = (rectangle) => {
    const { northEast, southWest } = rectangle;
    return {
        type: "Feature",
        geometry: {
            type: "Polygon",
            coordinates: [[
                [southWest.lng, southWest.lat],
                [northEast.lng, southWest.lat],
                [northEast.lng, northEast.lat],
                [southWest.lng, northEast.lat],
                [southWest.lng, southWest.lat]
            ]]
        },
        properties: {}
    };
};

export const isWithinFreeLimit = (area) => {
    const freeLimit = 1000000; // 1 km² in square meters
    return area <= freeLimit;
};