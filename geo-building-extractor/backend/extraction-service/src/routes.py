from flask import Blueprint, request, jsonify
from .extractor import extract_building_footprints
from .models import User, Order
from common.database import db_session

extraction_routes = Blueprint('extraction_routes', __name__)

@extraction_routes.route('/extract', methods=['POST'])
def extract():
    data = request.json
    user_id = data.get('user_id')
    rectangle = data.get('rectangle')  # Expecting a GeoJSON-like structure
    area = calculate_area(rectangle)

    if area <= 1:  # 1 km² free limit
        cost = 0
    else:
        cost = (area - 1) * 2  # $2 per square meter after the first km²

    # Check user balance and process payment if necessary
    user = db_session.query(User).filter_by(id=user_id).first()
    if user.balance < cost:
        return jsonify({'error': 'Insufficient balance'}), 403

    # Extract building footprints
    footprints = extract_building_footprints(rectangle)

    # Create an order record
    order = Order(user_id=user_id, area=area, cost=cost)
    db_session.add(order)
    user.balance -= cost
    db_session.commit()

    return jsonify({'footprints': footprints, 'cost': cost}), 200

def calculate_area(rectangle):
    # Implement area calculation logic based on the rectangle coordinates
    return abs((rectangle['coordinates'][0][0][0] - rectangle['coordinates'][0][1][0]) *
               (rectangle['coordinates'][0][0][1] - rectangle['coordinates'][0][2][1]))