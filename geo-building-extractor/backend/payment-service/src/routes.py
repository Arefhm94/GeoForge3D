from flask import Blueprint, request, jsonify
from .models import Payment
from .payment_processor import process_payment

payment_bp = Blueprint('payment', __name__)

@payment_bp.route('/create', methods=['POST'])
def create_payment():
    data = request.json
    user_id = data.get('user_id')
    amount = data.get('amount')

    if not user_id or not amount:
        return jsonify({'error': 'User ID and amount are required'}), 400

    payment = Payment(user_id=user_id, amount=amount)
    payment_id = process_payment(payment)

    if payment_id:
        return jsonify({'payment_id': payment_id}), 201
    else:
        return jsonify({'error': 'Payment processing failed'}), 500

@payment_bp.route('/status/<payment_id>', methods=['GET'])
def payment_status(payment_id):
    payment = Payment.query.get(payment_id)

    if payment:
        return jsonify({'payment_id': payment.id, 'status': payment.status}), 200
    else:
        return jsonify({'error': 'Payment not found'}), 404