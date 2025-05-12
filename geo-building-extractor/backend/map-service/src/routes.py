from flask import Blueprint, request, jsonify
from geo_utils import create_rectangle_geojson, extract_building_footprints
from common.database import get_user_data

map_routes = Blueprint('map_routes', __name__)

@map_routes.route('/create-rectangle', methods=['POST'])
def create_rectangle():
    data = request.json
    coordinates = data.get('coordinates')
    user_id = data.get('user_id')

    if not coordinates or not user_id:
        return jsonify({'error': 'Invalid input'}), 400

    geojson = create_rectangle_geojson(coordinates)
    return jsonify(geojson), 200

@map_routes.route('/extract-footprints', methods=['POST'])
def extract_footprints():
    data = request.json
    rectangle_geojson = data.get('rectangle_geojson')
    user_id = data.get('user_id')

    if not rectangle_geojson or not user_id:
        return jsonify({'error': 'Invalid input'}), 400

    footprints = extract_building_footprints(rectangle_geojson)
    return jsonify(footprints), 200

@map_routes.route('/user-data', methods=['GET'])
def user_data():
    user_id = request.args.get('user_id')

    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400

    user_info = get_user_data(user_id)
    return jsonify(user_info), 200