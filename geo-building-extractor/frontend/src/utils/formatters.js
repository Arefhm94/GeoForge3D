// This file contains functions for formatting data.

export const formatGeoJSON = (geoData) => {
    return {
        type: "FeatureCollection",
        features: geoData.map(feature => ({
            type: "Feature",
            geometry: feature.geometry,
            properties: feature.properties,
        })),
    };
};

export const formatArea = (areaInSquareMeters) => {
    if (areaInSquareMeters < 1000) {
        return `${areaInSquareMeters} m² (Free)`;
    }
    const chargeableArea = areaInSquareMeters - 1000;
    const cost = chargeableArea * 2; // $2 per square meter
    return `${areaInSquareMeters} m² (Total Cost: $${cost})`;
};

export const formatCoordinates = (coordinates) => {
    return coordinates.map(coord => ({
        lat: coord[1],
        lng: coord[0],
    }));
};