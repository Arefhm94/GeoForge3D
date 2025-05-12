from flask import Blueprint, request, jsonify
from shapely.geometry import box
import geojson
import json

extractor_bp = Blueprint('extractor', __name__)

@extractor_bp.route('/extract', methods=['POST'])
def extract_building_footprints():
    data = request.json
    if 'rectangle' not in data:
        return jsonify({'error': 'No rectangle provided'}), 400

    rectangle = data['rectangle']
    if not validate_rectangle(rectangle):
        return jsonify({'error': 'Invalid rectangle coordinates'}), 400

    geojson_data = create_geojson(rectangle)
    footprints = get_building_footprints(geojson_data)

    return jsonify(footprints), 200

def validate_rectangle(rectangle):
    if len(rectangle) != 4:
        return False
    return all(isinstance(coord, (int, float)) for coord in rectangle)

def create_geojson(rectangle):
    min_x, min_y, max_x, max_y = rectangle
    geom = box(min_x, min_y, max_x, max_y)
    return geojson.Feature(geometry=geojson.loads(geom.to_geojson()))

def get_building_footprints(geojson_data):
    # Placeholder for actual building footprint extraction logic
    return {
        "type": "FeatureCollection",
        "features": []
    }