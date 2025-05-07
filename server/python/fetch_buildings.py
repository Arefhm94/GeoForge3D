#!/usr/bin/env python3
"""
Building Footprints Fetcher

This script fetches building footprints from OpenStreetMap and Microsoft Building Footprints
for a specified bounding box and returns them in GeoJSON format.

Usage:
    python fetch_buildings.py --west LONGITUDE --south LATITUDE --east LONGITUDE --north LATITUDE 
                             [--sources osm,microsoft] [--output FILENAME]
"""

import os
import sys
import json
import argparse
import tempfile
import requests

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

def fetch_combined_buildings(bounds, sources=None):
    """
    Fetch building footprints from multiple sources and combine them.
    
    Args:
        bounds: A dictionary containing the bounding box coordinates.
        sources: A list of sources to use. Options are 'osm' and 'microsoft'.
                If None, all sources are used.
                
    Returns:
        A GeoJSON object containing building footprints from all sources.
    """
    if sources is None:
        sources = ['osm', 'microsoft']
    
    all_features = []
    errors = []
    
    # Fetch from OpenStreetMap
    if 'osm' in sources:
        try:
            osm_data = fetch_osm_buildings(bounds)
            if 'error' in osm_data:
                errors.append(osm_data['error'])
            else:
                all_features.extend(osm_data.get('features', []))
        except Exception as e:
            errors.append(f"Error fetching OSM data: {str(e)}")
    
    # Fetch from Microsoft
    if 'microsoft' in sources:
        try:
            ms_data = fetch_microsoft_buildings(bounds)
            if 'error' in ms_data:
                errors.append(ms_data['error'])
            else:
                all_features.extend(ms_data.get('features', []))
        except Exception as e:
            errors.append(f"Error fetching Microsoft data: {str(e)}")
    
    # Create combined GeoJSON
    combined_geojson = {
        "type": "FeatureCollection",
        "features": all_features,
        "sources": sources
    }
    
    if errors:
        combined_geojson["errors"] = errors
    
    return combined_geojson

def save_geojson_to_file(geojson_data, filename=None):
    """
    Save GeoJSON data to a file.
    
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

def fetch_and_save_buildings(bounds, sources=None, output_file=None):
    """
    Fetch building footprints and save them to a file.
    
    Args:
        bounds: A dictionary containing the bounding box coordinates.
        sources: A list of sources to use.
        output_file: The file to save to. If None, a temporary file is created.
        
    Returns:
        A dictionary with the GeoJSON data and the path to the saved file.
    """
    combined_data = fetch_combined_buildings(bounds, sources)
    filepath = save_geojson_to_file(combined_data, output_file)
    
    return {
        "geojson": combined_data,
        "filepath": filepath
    }

def main():
    """
    Main function to be run from the command line.
    """
    parser = argparse.ArgumentParser(description='Fetch building footprints from various sources.')
    parser.add_argument('--west', type=float, required=True, help='Western boundary (longitude)')
    parser.add_argument('--south', type=float, required=True, help='Southern boundary (latitude)')
    parser.add_argument('--east', type=float, required=True, help='Eastern boundary (longitude)')
    parser.add_argument('--north', type=float, required=True, help='Northern boundary (latitude)')
    parser.add_argument('--sources', type=str, default='osm,microsoft', 
                       help='Comma-separated list of sources (osm,microsoft)')
    parser.add_argument('--output', type=str, help='Output file path')
    parser.add_argument('--format', choices=['geojson', 'filepath'], default='filepath',
                       help='Output format: "geojson" for the full GeoJSON object or "filepath" for just the path to the saved file')
    
    args = parser.parse_args()
    
    bounds = {
        'west': args.west,
        'south': args.south,
        'east': args.east,
        'north': args.north
    }
    
    sources = args.sources.split(',')
    
    result = fetch_and_save_buildings(bounds, sources, args.output)
    
    # Output either the filepath or the full GeoJSON
    if args.format == 'filepath':
        print(result['filepath'])
    else:
        print(json.dumps(result['geojson']))
    
    return 0

if __name__ == '__main__':
    sys.exit(main())