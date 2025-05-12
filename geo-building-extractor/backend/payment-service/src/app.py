from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import Payment
from payment_processor import process_payment

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///payments.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

@app.route('/api/payments', methods=['POST'])
def create_payment():
    data = request.json
    amount = data.get('amount')
    user_id = data.get('user_id')

    if not amount or not user_id:
        return jsonify({'error': 'Amount and user_id are required'}), 400

    payment = Payment(amount=amount, user_id=user_id)
    db.session.add(payment)
    db.session.commit()

    payment_status = process_payment(payment)

    return jsonify({'payment_id': payment.id, 'status': payment_status}), 201

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)