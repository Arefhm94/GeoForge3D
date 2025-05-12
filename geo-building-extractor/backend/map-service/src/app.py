from flask import Flask, request, jsonify
from flask_cors import CORS
from geo_utils import calculate_area, extract_building_footprints

app = Flask(__name__)
CORS(app)

@app.route('/api/rectangle', methods=['POST'])
def create_rectangle():
    data = request.json
    coordinates = data.get('coordinates')
    
    if not coordinates or len(coordinates) != 4:
        return jsonify({'error': 'Invalid coordinates'}), 400
    
    area = calculate_area(coordinates)
    if area <= 1000000:  # 1 km² in square meters
        return jsonify({'message': 'Rectangle created', 'area': area}), 200
    else:
        cost = (area - 1000000) * 2  # $2 per square meter after the first km²
        return jsonify({'message': 'Rectangle created', 'area': area, 'cost': cost}), 200

@app.route('/api/extract', methods=['POST'])
def extract_data():
    data = request.json
    coordinates = data.get('coordinates')
    
    if not coordinates or len(coordinates) != 4:
        return jsonify({'error': 'Invalid coordinates'}), 400
    
    footprints = extract_building_footprints(coordinates)
    return jsonify({'footprints': footprints}), 200

if __name__ == '__main__':
    app.run(debug=True)