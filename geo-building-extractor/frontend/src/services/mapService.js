import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000'; // Adjust the base URL as needed

export const getBuildingFootprints = async (rectangle) => {
    try {
        const response = await axios.post(`${API_BASE_URL}/map/building-footprints`, rectangle);
        return response.data;
    } catch (error) {
        console.error('Error fetching building footprints:', error);
        throw error;
    }
};

export const exportGeoJSON = (rectangle) => {
    const geoJSON = {
        type: 'FeatureCollection',
        features: [
            {
                type: 'Feature',
                geometry: {
                    type: 'Polygon',
                    coordinates: [[
                        [rectangle.startLng, rectangle.startLat],
                        [rectangle.endLng, rectangle.startLat],
                        [rectangle.endLng, rectangle.endLat],
                        [rectangle.startLng, rectangle.endLat],
                        [rectangle.startLng, rectangle.startLat]
                    ]]
                },
                properties: {}
            }
        ]
    };
    return geoJSON;
};