from flask import Blueprint, request, jsonify
from services.geo_service import get_map_data, export_geojson
from services.building_extraction import extract_building_footprints

map_data_bp = Blueprint('map_data', __name__)

@map_data_bp.route('/map/data', methods=['GET'])
def map_data():
    location = request.args.get('location')
    zoom_level = request.args.get('zoom', default=10, type=int)
    data = get_map_data(location, zoom_level)
    return jsonify(data)

@map_data_bp.route('/map/export_geojson', methods=['POST'])
def export_geojson_endpoint():
    rectangle = request.json.get('rectangle')
    geojson = export_geojson(rectangle)
    return jsonify(geojson)

@map_data_bp.route('/map/buildings', methods=['POST'])
def buildings():
    rectangle = request.json.get('rectangle')
    footprints = extract_building_footprints(rectangle)
    return jsonify(footprints)