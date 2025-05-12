"""
Microsoft Building Footprints Fetcher

This module provides functions to fetch building footprints from Microsoft's
open building footprints dataset using their REST API.
"""

import os
import json
import requests
import tempfile

def fetch_microsoft_buildings(bounds):
    """
    Fetch building footprints from Microsoft Building Footprints API.
    
    Microsoft provides a REST API to query their global building footprints dataset.
    This function converts the bounding box to the format expected by the API,
    makes the request, and returns the results as GeoJSON.
    
    Args:
        bounds: A dictionary containing the bounding box coordinates with 
               keys 'north', 'south', 'east', 'west'.
               
    Returns:
        A GeoJSON object containing building footprints.
    """
    # Extract bounds
    south = bounds['south']
    west = bounds['west']
    north = bounds['north']
    east = bounds['east']
    
    # Check if the area is too large
    area = (north - south) * (east - west)
    if area > 0.1:  # Roughly about 10km x 10km
        return {
            "type": "FeatureCollection", 
            "features": [],
            "error": "Area too large. Please select a smaller area."
        }
    
    # Microsoft Building Footprints API endpoint
    # This uses the Open Buildings API from Microsoft
    api_url = "https://tiles.openmicrosoft.com/api/buildings/v1/query"
    
    # Format the bounding box for the API
    bbox = f"{west},{south},{east},{north}"
    
    # Set up the request parameters
    params = {
        "bbox": bbox,
        "limit": 10000,  # Maximum number of buildings to return
        "format": "geojson"
    }
    
    try:
        # Make the API request
        response = requests.get(api_url, params=params)
        
        if response.status_code != 200:
            return {
                "type": "FeatureCollection",
                "features": [],
                "error": f"Failed to fetch data from Microsoft API: {response.status_code}"
            }
        
        # Parse the response
        ms_data = response.json()
        
        # Add source property to each feature
        if "features" in ms_data:
            for feature in ms_data["features"]:
                if "properties" not in feature:
                    feature["properties"] = {}
                feature["properties"]["source"] = "Microsoft Building Footprints"
        
        # Add source property to the collection
        ms_data["source"] = "Microsoft Building Footprints"
        
        return ms_data
        
    except Exception as e:
        return {
            "type": "FeatureCollection",
            "features": [],
            "error": f"Error fetching Microsoft building data: {str(e)}"
        }

def save_geojson_to_file(geojson_data, filename=None):
    """
    Save GeoJSON data to a temporary file.
    
    Args:
        geojson_data: The GeoJSON data to save.
        filename: The filename to save to. If None, a temporary file is created.
        
    Returns:
        The path to the saved file.
    """
    if filename is None:
        fd, filename = tempfile.mkstemp(suffix='.geojson')
        os.close(fd)
    
    with open(filename, 'w') as f:
        json.dump(geojson_data, f)
    
    return filename

def fetch_and_save_microsoft_buildings(bounds):
    """
    Fetch building footprints from Microsoft and save to a file.
    
    Args:
        bounds: A dictionary containing the bounding box coordinates.
        
    Returns:
        A dictionary with the GeoJSON data and the path to the saved file.
    """
    geojson_data = fetch_microsoft_buildings(bounds)
    filepath = save_geojson_to_file(geojson_data)
    
    return {
        "geojson": geojson_data,
        "filepath": filepath
    }