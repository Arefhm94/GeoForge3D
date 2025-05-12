from flask import Flask, request, jsonify
from flask_cors import CORS
from extractor import extract_building_footprints
from models import User, Order
from common.database import db_session

app = Flask(__name__)
CORS(app)

@app.route('/extract', methods=['POST'])
def extract():
    data = request.json
    user_id = data.get('user_id')
    rectangle = data.get('rectangle')  # Expecting a GeoJSON-like structure
    area = calculate_area(rectangle)

    if area <= 1000000:  # 1 km² in square meters
        cost = 0
    else:
        cost = (area - 1000000) * 2  # $2 per square meter after the first km²

    # Check user balance and create order logic here
    user = db_session.query(User).filter_by(id=user_id).first()
    if user.balance < cost:
        return jsonify({'error': 'Insufficient balance'}), 400

    footprints = extract_building_footprints(rectangle)
    order = Order(user_id=user_id, area=area, cost=cost)
    db_session.add(order)
    db_session.commit()

    return jsonify({'footprints': footprints, 'cost': cost}), 200

def calculate_area(rectangle):
    # Implement area calculation logic based on the rectangle coordinates
    return abs((rectangle['coordinates'][0][0][0] - rectangle['coordinates'][0][1][0]) *
               (rectangle['coordinates'][0][0][1] - rectangle['coordinates'][0][2][1]))

if __name__ == '__main__':
    app.run(debug=True)