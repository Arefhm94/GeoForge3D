// This file contains utility functions for geo-related operations.

export const createGeoJSONRectangle = (coordinates: [number, number][]) => {
    return {
        type: "Feature",
        geometry: {
            type: "Polygon",
            coordinates: [coordinates],
        },
        properties: {},
    };
};

export const calculateArea = (coordinates: [number, number][]) => {
    // Simple calculation for area in square meters based on coordinates
    // This is a placeholder and should be replaced with a proper area calculation
    const length = Math.abs(coordinates[0][0] - coordinates[2][0]);
    const width = Math.abs(coordinates[0][1] - coordinates[1][1]);
    return length * width; // This is a simplistic approach
};

export const extractBuildingFootprints = async (rectangle: any) => {
    // Placeholder for API call to extract building footprints
    // This function should call the backend service to get the footprints based on the rectangle
    const response = await fetch('/api/geo/extract', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(rectangle),
    });
    return response.json();
};