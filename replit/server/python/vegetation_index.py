#!/usr/bin/env python
import json
import sys
import random

def analyze_vegetation(geojson_path, options):
    """
    Simulates vegetation index analysis on the provided GeoJSON.
    In a real implementation, this would use satellite imagery and NDVI calculations.
    
    Args:
        geojson_path: Path to the input GeoJSON file
        options: JSON string containing analysis options
    
    Returns:
        JSON with vegetation analysis results
    """
    # Parse the GeoJSON file
    with open(geojson_path, 'r') as f:
        geojson = json.load(f)
    
    # Parse options
    options_dict = json.loads(options)
    
    # Get the index type from options
    index_type = options_dict.get('indexType', 'ndvi')  # NDVI is default
    
    # Simulate vegetation index data
    mean_index = random.uniform(0.4, 0.7)
    min_index = max(0, mean_index - random.uniform(0.2, 0.4))
    max_index = min(1, mean_index + random.uniform(0.1, 0.3))
    
    # Generate distribution data for the histogram
    distribution = []
    # NDVI categories with their ranges
    categories = [
        {"label": "No vegetation", "min": 0.0, "max": 0.2, "color": "bg-gray-500"},
        {"label": "Sparse vegetation", "min": 0.2, "max": 0.4, "color": "bg-yellow-500"},
        {"label": "Moderate vegetation", "min": 0.4, "max": 0.6, "color": "bg-lime-500"},
        {"label": "Dense vegetation", "min": 0.6, "max": 0.8, "color": "bg-green-500"},
        {"label": "Very dense vegetation", "min": 0.8, "max": 1.0, "color": "bg-emerald-700"}
    ]
    
    # Generate percentage for each category (ensure they sum to 100%)
    total = 0
    for i, category in enumerate(categories[:-1]):
        if i == 0:
            # First category usually has less
            percentage = random.uniform(0, 15)
        else:
            percentage = random.uniform(10, 30)
        distribution.append({
            "label": category["label"],
            "percentage": round(percentage, 1),
            "color": category["color"],
            "range": [category["min"], category["max"]]
        })
        total += percentage
    
    # Last category gets the remainder to ensure 100%
    distribution.append({
        "label": categories[-1]["label"],
        "percentage": round(100 - total, 1),
        "color": categories[-1]["color"],
        "range": [categories[-1]["min"], categories[-1]["max"]]
    })
    
    # Sort by percentage (highest first)
    distribution.sort(key=lambda x: x["percentage"], reverse=True)
    
    # Get dominant category (highest percentage)
    dominant_category = distribution[0]["label"]
    
    result = {
        'indexType': index_type.upper(),
        'statistics': {
            'mean': round(mean_index, 2),
            'min': round(min_index, 2),
            'max': round(max_index, 2),
            'standardDeviation': round(random.uniform(0.05, 0.15), 2)
        },
        'distribution': distribution,
        'summary': [
            f"The selected area has a mean {index_type.upper()} value of {round(mean_index, 2)}, indicating {dominant_category.lower()}.",
            f"Vegetation health appears to be {random.choice(['excellent', 'good', 'moderate', 'variable'])} across the selected region.",
            f"The distribution analysis shows that {distribution[0]['percentage']}% of the area consists of {distribution[0]['label'].lower()}.",
            "Areas with lower vegetation indices may benefit from targeted conservation or restoration efforts."
        ]
    }
    
    return result

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(json.dumps({"error": "Missing arguments. Usage: vegetation_index.py geojson_path options_json"}))
        sys.exit(1)
    
    geojson_path = sys.argv[1]
    options = sys.argv[2]
    
    try:
        result = analyze_vegetation(geojson_path, options)
        print(json.dumps(result))
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)
