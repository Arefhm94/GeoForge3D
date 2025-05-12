from flask import Blueprint, request, jsonify
from services.building_extraction import extract_building_footprints

buildings_bp = Blueprint('buildings', __name__)

@buildings_bp.route('/extract', methods=['POST'])
def extract():
    data = request.json
    if 'rectangle' not in data:
        return jsonify({'error': 'Rectangle data is required'}), 400

    rectangle = data['rectangle']
    footprints = extract_building_footprints(rectangle)

    return jsonify(footprints)