"""
Main Building Footprints Module

This module provides a unified interface to fetch building footprints
from multiple sources (OpenStreetMap and Microsoft Building Footprints).
"""

import os
import sys
import json
import argparse
import tempfile
from .osm_buildings import fetch_osm_buildings
from .microsoft_buildings import fetch_microsoft_buildings

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
    
    args = parser.parse_args()
    
    bounds = {
        'west': args.west,
        'south': args.south,
        'east': args.east,
        'north': args.north
    }
    
    sources = args.sources.split(',')
    
    result = fetch_and_save_buildings(bounds, sources, args.output)
    
    # Print the filepath for the calling program to use
    print(result['filepath'])
    
    return 0

if __name__ == '__main__':
    sys.exit(main())