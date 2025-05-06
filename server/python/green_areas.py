#!/usr/bin/env python
import json
import sys
import random

def analyze_green_areas(geojson_path, options):
    """
    Simulates green areas analysis on the provided GeoJSON.
    In a real implementation, this would use satellite imagery and vegetation detection.
    
    Args:
        geojson_path: Path to the input GeoJSON file
        options: JSON string containing analysis options
    
    Returns:
        JSON with green areas analysis results
    """
    # Parse the GeoJSON file
    with open(geojson_path, 'r') as f:
        geojson = json.load(f)
    
    # Parse options
    options_dict = json.loads(options)
    
    # Get options
    detail_level = options_dict.get('detailLevel', 'medium')
    
    # Simulate green space distribution
    total_green_percent = random.uniform(20, 55)
    
    # Types of green spaces
    green_space_types = [
        {"type": "Parks", "percentage": round(random.uniform(15, 40), 1), "color": "bg-emerald-500"},
        {"type": "Urban Forests", "percentage": round(random.uniform(10, 30), 1), "color": "bg-green-700"},
        {"type": "Street Trees", "percentage": round(random.uniform(5, 15), 1), "color": "bg-lime-500"},
        {"type": "Private Gardens", "percentage": round(random.uniform(10, 25), 1), "color": "bg-green-500"},
        {"type": "Agricultural Land", "percentage": round(random.uniform(0, 15), 1), "color": "bg-yellow-600"},
        {"type": "Vacant Green Lots", "percentage": round(random.uniform(0, 10), 1), "color": "bg-lime-300"}
    ]
    
    # Ensure percentages sum to 100%
    total = sum(item["percentage"] for item in green_space_types)
    for item in green_space_types:
        item["percentage"] = round((item["percentage"] / total) * 100, 1)
    
    # Sort by percentage (highest first)
    green_space_types.sort(key=lambda x: x["percentage"], reverse=True)
    
    # Ecological metrics
    biodiversity_score = round(random.uniform(40, 95), 1)
    connectivity_score = round(random.uniform(30, 90), 1)
    carbon_sequestration = round(random.uniform(5, 30), 1)  # Tons per hectare per year
    
    # Benefits analysis
    air_quality_improvement = round(random.uniform(5, 25), 1)  # Percent improvement
    temperature_reduction = round(random.uniform(1, 5), 1)     # Degrees C
    stormwater_managed = round(random.uniform(10, 60), 1)      # Percent of rainfall
    
    result = {
        'greenCoverage': {
            'totalPercentage': round(total_green_percent, 1),
            'greenSpaceTypes': green_space_types
        },
        'ecologicalMetrics': {
            'biodiversityScore': biodiversity_score,
            'habitatConnectivity': connectivity_score,
            'carbonSequestration': carbon_sequestration
        },
        'benefits': {
            'airQualityImprovement': air_quality_improvement,
            'urbanHeatIslandMitigation': temperature_reduction,
            'stormwaterManagement': stormwater_managed
        },
        'summary': [
            f"The selected area has approximately {round(total_green_percent, 1)}% green space coverage.",
            f"The predominant green space type is {green_space_types[0]['type']} ({green_space_types[0]['percentage']}%), followed by {green_space_types[1]['type']} ({green_space_types[1]['percentage']}%).",
            f"These green spaces provide significant ecosystem services, including air quality improvement of {air_quality_improvement}% and temperature reduction of {temperature_reduction}°C.",
            f"The biodiversity score of {biodiversity_score} indicates a {get_biodiversity_rating(biodiversity_score)} level of species diversity."
        ]
    }
    
    return result

def get_biodiversity_rating(score):
    if score < 50:
        return "low"
    elif score < 75:
        return "moderate"
    else:
        return "high"

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(json.dumps({"error": "Missing arguments. Usage: green_areas.py geojson_path options_json"}))
        sys.exit(1)
    
    geojson_path = sys.argv[1]
    options = sys.argv[2]
    
    try:
        result = analyze_green_areas(geojson_path, options)
        print(json.dumps(result))
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)