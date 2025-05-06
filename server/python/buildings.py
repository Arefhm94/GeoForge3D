#!/usr/bin/env python
import json
import sys
import random

def analyze_buildings(geojson_path, options):
    """
    Simulates building detection analysis on the provided GeoJSON.
    In a real implementation, this would use machine learning on satellite imagery.
    
    Args:
        geojson_path: Path to the input GeoJSON file
        options: JSON string containing analysis options
    
    Returns:
        JSON with building detection results
    """
    # Parse the GeoJSON file
    with open(geojson_path, 'r') as f:
        geojson = json.load(f)
    
    # Parse options
    options_dict = json.loads(options)
    
    # Get options
    detection_confidence = options_dict.get('detectionConfidence', 'high')
    
    # Simulate building data
    building_count = random.randint(25, 800)
    building_density = round(random.uniform(10, 70), 1)  # Buildings per hectare
    total_footprint_area = round(random.uniform(5000, 100000), 1)  # Square meters
    average_height = round(random.uniform(5, 50), 1)  # Meters
    
    # Building types
    building_types = [
        {"type": "Residential", "count": round(building_count * random.uniform(0.4, 0.7)), "color": "bg-blue-500"},
        {"type": "Commercial", "count": round(building_count * random.uniform(0.1, 0.3)), "color": "bg-purple-500"},
        {"type": "Industrial", "count": round(building_count * random.uniform(0.05, 0.2)), "color": "bg-slate-600"},
        {"type": "Institutional", "count": round(building_count * random.uniform(0.03, 0.1)), "color": "bg-amber-500"},
        {"type": "Mixed-Use", "count": round(building_count * random.uniform(0.05, 0.15)), "color": "bg-teal-500"}
    ]
    
    # Adjust counts to sum to building_count
    total = sum(item["count"] for item in building_types)
    adjustment_factor = building_count / total
    
    for item in building_types:
        item["count"] = round(item["count"] * adjustment_factor)
        item["percentage"] = round((item["count"] / building_count) * 100, 1)
    
    # Sort by count (highest first)
    building_types.sort(key=lambda x: x["count"], reverse=True)
    
    # Ensure total matches building_count after rounding errors
    difference = building_count - sum(item["count"] for item in building_types)
    if difference != 0:
        building_types[0]["count"] += difference
        
    # Update percentages after adjustment
    for item in building_types:
        item["percentage"] = round((item["count"] / building_count) * 100, 1)
    
    # Building age distribution (years)
    age_distribution = [
        {"range": "< 10", "percentage": round(random.uniform(5, 25), 1)},
        {"range": "10-25", "percentage": round(random.uniform(10, 30), 1)},
        {"range": "25-50", "percentage": round(random.uniform(20, 40), 1)},
        {"range": "50-100", "percentage": round(random.uniform(10, 30), 1)},
        {"range": "> 100", "percentage": round(random.uniform(0, 15), 1)}
    ]
    
    # Ensure percentages sum to 100%
    total = sum(item["percentage"] for item in age_distribution)
    for item in age_distribution:
        item["percentage"] = round((item["percentage"] / total) * 100, 1)
    
    # Built environment metrics
    floor_area_ratio = round(random.uniform(0.5, 10), 1)
    lot_coverage = round(random.uniform(20, 80), 1)  # Percentage
    
    result = {
        'buildingStatistics': {
            'count': building_count,
            'density': building_density,
            'totalFootprintArea': total_footprint_area,
            'averageHeight': average_height,
            'floorAreaRatio': floor_area_ratio,
            'lotCoverage': lot_coverage
        },
        'buildingTypes': building_types,
        'ageDistribution': age_distribution,
        'summary': [
            f"The selected area contains {building_count} buildings with a density of {building_density} buildings per hectare.",
            f"The predominant building type is {building_types[0]['type']} ({building_types[0]['percentage']}%).",
            f"Buildings cover approximately {lot_coverage}% of the land area with a total footprint of {total_footprint_area} square meters.",
            f"The average building height is {average_height} meters, and {age_distribution[0]['percentage']}% of buildings are {age_distribution[0]['range']} years old."
        ]
    }
    
    return result

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(json.dumps({"error": "Missing arguments. Usage: buildings.py geojson_path options_json"}))
        sys.exit(1)
    
    geojson_path = sys.argv[1]
    options = sys.argv[2]
    
    try:
        result = analyze_buildings(geojson_path, options)
        print(json.dumps(result))
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)