from flask import Blueprint, request, jsonify
from services.payment_service import process_payment, calculate_fee
from models.order import Order
from models.user import User

payments_bp = Blueprint('payments', __name__)

@payments_bp.route('/api/payments', methods=['POST'])
def handle_payment():
    data = request.json
    user_id = data.get('user_id')
    area_size = data.get('area_size')  # in square meters

    user = User.get_user_by_id(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    fee = calculate_fee(area_size)
    if fee > user.balance:
        return jsonify({'error': 'Insufficient balance'}), 400

    payment_successful = process_payment(user, fee)
    if payment_successful:
        order = Order(user_id=user_id, area_size=area_size, fee=fee)
        order.save()
        return jsonify({'message': 'Payment successful', 'order_id': order.id}), 200
    else:
        return jsonify({'error': 'Payment processing failed'}), 500