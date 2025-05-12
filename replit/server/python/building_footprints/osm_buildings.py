"""
OpenStreetMap Building Footprints Fetcher

This module provides functions to fetch building footprints from OpenStreetMap
for a given bounding box.
"""

import os
import json
import requests
import tempfile

def fetch_osm_buildings(bounds):
    """
    Fetch building footprints from OpenStreetMap Overpass API.
    
    Args:
        bounds: A dictionary containing the bounding box coordinates with 
               keys 'north', 'south', 'east', 'west'.
               
    Returns:
        A GeoJSON object containing building footprints as a collection of polygons.
    """
    # Extract bounds
    south = bounds['south']
    west = bounds['west']
    north = bounds['north']
    east = bounds['east']
    
    # Check if the area is too large (prevent overloading Overpass API)
    area = (north - south) * (east - west)
    if area > 0.1:  # Roughly about 10km x 10km
        return {
            "type": "FeatureCollection", 
            "features": [],
            "error": "Area too large. Please select a smaller area."
        }
    
    # Build Overpass API query
    # This query fetches all buildings in the bounding box
    overpass_url = "https://overpass-api.de/api/interpreter"
    overpass_query = f"""
    [out:json];
    (
      way["building"]({south},{west},{north},{east});
      relation["building"]({south},{west},{north},{east});
    );
    out body;
    >;
    out skel qt;
    """
    
    try:
        # Make the API request
        response = requests.post(overpass_url, data={"data": overpass_query})
        
        if response.status_code != 200:
            return {
                "type": "FeatureCollection",
                "features": [],
                "error": f"Failed to fetch data from Overpass API: {response.status_code}"
            }
        
        # Parse the response
        osm_data = response.json()
        
        # Process the data into GeoJSON
        return convert_osm_to_geojson(osm_data)
        
    except Exception as e:
        return {
            "type": "FeatureCollection",
            "features": [],
            "error": f"Error fetching OSM data: {str(e)}"
        }

def convert_osm_to_geojson(osm_data):
    """
    Convert OSM data to GeoJSON format.
    
    Args:
        osm_data: The OSM data from Overpass API.
        
    Returns:
        A GeoJSON object.
    """
    # Create a lookup of nodes by ID
    nodes = {}
    for element in osm_data['elements']:
        if element['type'] == 'node':
            nodes[element['id']] = {
                'lat': element['lat'],
                'lon': element['lon']
            }
    
    # Process ways (buildings)
    features = []
    
    for element in osm_data['elements']:
        if element['type'] == 'way' and 'tags' in element and 'building' in element['tags']:
            # Get coordinates for each node in the way
            coords = []
            for node_id in element['nodes']:
                if node_id in nodes:
                    coords.append([
                        nodes[node_id]['lon'],
                        nodes[node_id]['lat']
                    ])
            
            # Ensure the polygon is closed
            if coords and coords[0] != coords[-1]:
                coords.append(coords[0])
            
            if len(coords) >= 4:  # Minimum 3 points + closing point
                # Create a GeoJSON feature
                feature = {
                    "type": "Feature",
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [coords]
                    },
                    "properties": {
                        "id": element['id'],
                        "source": "OpenStreetMap"
                    }
                }
                
                # Add tags as properties
                if 'tags' in element:
                    for key, value in element['tags'].items():
                        feature['properties'][key] = value
                
                features.append(feature)
    
    return {
        "type": "FeatureCollection",
        "features": features,
        "source": "OpenStreetMap"
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

def fetch_and_save_osm_buildings(bounds):
    """
    Fetch building footprints from OpenStreetMap and save to a file.
    
    Args:
        bounds: A dictionary containing the bounding box coordinates.
        
    Returns:
        A dictionary with the GeoJSON data and the path to the saved file.
    """
    geojson_data = fetch_osm_buildings(bounds)
    filepath = save_geojson_to_file(geojson_data)
    
    return {
        "geojson": geojson_data,
        "filepath": filepath
    }