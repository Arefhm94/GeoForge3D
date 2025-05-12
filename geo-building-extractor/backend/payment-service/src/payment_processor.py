from decimal import Decimal
import stripe
from flask import Blueprint, request, jsonify
from backend.common.database import get_db

payment_bp = Blueprint('payment', __name__)

# Initialize Stripe with your secret key
stripe.api_key = 'your_stripe_secret_key'

@payment_bp.route('/create-payment-intent', methods=['POST'])
def create_payment():
    data = request.json
    user_id = data.get('user_id')
    area_size = data.get('area_size')  # in square meters

    if area_size <= 1000000:  # 1 km²
        amount = 0  # Free for the first 1 km²
    else:
        amount = (area_size - 1000000) * 2  # $2 per square meter after the first 1 km²

    try:
        payment_intent = stripe.PaymentIntent.create(
            amount=int(amount * 100),  # Amount in cents
            currency='usd',
            metadata={'user_id': user_id}
        )
        return jsonify({'client_secret': payment_intent['client_secret']}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@payment_bp.route('/payment-success', methods=['POST'])
def payment_success():
    data = request.json
    user_id = data.get('user_id')
    payment_intent_id = data.get('payment_intent_id')

    db = get_db()
    cursor = db.cursor()

    # Record the payment in the database
    cursor.execute(
        "INSERT INTO payments (user_id, payment_intent_id) VALUES (?, ?)",
        (user_id, payment_intent_id)
    )
    db.commit()

    return jsonify({'message': 'Payment recorded successfully'}), 200

@payment_bp.route('/payment-history/<user_id>', methods=['GET'])
def payment_history(user_id):
    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM payments WHERE user_id = ?", (user_id,))
    payments = cursor.fetchall()

    return jsonify(payments), 200