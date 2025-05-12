#!/usr/bin/env python
import json
import sys
import random

def analyze_terrain(geojson_path, options):
    """
    Simulates terrain analysis on the provided GeoJSON.
    In a real implementation, this would use DEMs and GIS libraries.
    
    Args:
        geojson_path: Path to the input GeoJSON file
        options: JSON string containing analysis options
    
    Returns:
        JSON with terrain analysis results
    """
    # Parse the GeoJSON file
    with open(geojson_path, 'r') as f:
        geojson = json.load(f)
    
    # Parse options
    options_dict = json.loads(options)
    
    # Get options
    resolution = options_dict.get('resolution', 'medium')
    
    # Simulated terrain statistics
    min_elevation = random.randint(0, 300)
    max_elevation = min_elevation + random.randint(50, 500)
    mean_elevation = round((min_elevation + max_elevation) / 2, 1)
    median_elevation = round(mean_elevation + random.uniform(-50, 50), 1)
    
    # Terrain metrics
    mean_slope = round(random.uniform(0, 45), 1)  # Degrees
    max_slope = round(min(mean_slope + random.uniform(5, 30), 90), 1)  # Degrees
    ruggedness_index = round(random.uniform(0, 1), 3)  # 0-1 scale
    
    # Aspect distribution (N, E, S, W)
    aspect_distribution = [
        {"direction": "North", "percentage": round(random.uniform(10, 35), 1)},
        {"direction": "East", "percentage": round(random.uniform(10, 35), 1)},
        {"direction": "South", "percentage": round(random.uniform(10, 35), 1)},
        {"direction": "West", "percentage": round(random.uniform(10, 35), 1)}
    ]
    
    # Ensure percentages sum to 100%
    total = sum(item["percentage"] for item in aspect_distribution)
    for item in aspect_distribution:
        item["percentage"] = round((item["percentage"] / total) * 100, 1)
        
    # Sort by percentage (highest first)
    aspect_distribution.sort(key=lambda x: x["percentage"], reverse=True)
    
    # Landform classification
    landform_types = [
        {"type": "Plains", "percentage": round(random.uniform(0, 50), 1), "color": "bg-lime-200"},
        {"type": "Hills", "percentage": round(random.uniform(0, 50), 1), "color": "bg-amber-300"},
        {"type": "Valleys", "percentage": round(random.uniform(0, 30), 1), "color": "bg-emerald-400"},
        {"type": "Ridges", "percentage": round(random.uniform(0, 20), 1), "color": "bg-stone-400"},
        {"type": "Peaks", "percentage": round(random.uniform(0, 10), 1), "color": "bg-slate-500"}
    ]
    
    # Ensure percentages sum to 100%
    total = sum(item["percentage"] for item in landform_types)
    for item in landform_types:
        item["percentage"] = round((item["percentage"] / total) * 100, 1)
        
    # Sort by percentage (highest first)
    landform_types.sort(key=lambda x: x["percentage"], reverse=True)
    
    # Generate elevation profile points
    profile_points = 20
    profile_data = []
    for i in range(profile_points):
        x_percent = (i / (profile_points - 1)) * 100
        elevation = min_elevation + random.uniform(0, max_elevation - min_elevation)
        profile_data.append({
            'position': x_percent,
            'elevation': round(elevation, 1)
        })
    
    # Sort by position to ensure correct rendering
    profile_data.sort(key=lambda x: x['position'])
    
    result = {
        'elevationStatistics': {
            'minimum': min_elevation,
            'maximum': max_elevation,
            'mean': mean_elevation,
            'median': median_elevation,
            'range': max_elevation - min_elevation
        },
        'terrainMetrics': {
            'meanSlope': mean_slope,
            'maxSlope': max_slope,
            'terrainRuggednessIndex': ruggedness_index
        },
        'aspectDistribution': aspect_distribution,
        'landformClassification': landform_types,
        'elevationProfile': profile_data,
        'summary': [
            f"The selected area has an elevation range from {min_elevation}m to {max_elevation}m above sea level.",
            f"The terrain is predominantly {landform_types[0]['type']} ({landform_types[0]['percentage']}%) with a mean slope of {mean_slope}°.",
            f"The terrain ruggedness index of {ruggedness_index} indicates a {get_ruggedness_description(ruggedness_index)} landscape.",
            f"Most slopes in the area face {aspect_distribution[0]['direction']} ({aspect_distribution[0]['percentage']}%)."
        ]
    }
    
    return result

def get_ruggedness_description(index):
    if index < 0.2:
        return "very smooth"
    elif index < 0.4:
        return "relatively smooth"
    elif index < 0.6:
        return "moderately rugged"
    elif index < 0.8:
        return "rugged"
    else:
        return "very rugged"

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(json.dumps({"error": "Missing arguments. Usage: terrain.py geojson_path options_json"}))
        sys.exit(1)
    
    geojson_path = sys.argv[1]
    options = sys.argv[2]
    
    try:
        result = analyze_terrain(geojson_path, options)
        print(json.dumps(result))
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)