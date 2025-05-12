from flask import jsonify
from decimal import Decimal

class PaymentService:
    def __init__(self):
        self.free_limit = Decimal('1.0')  # 1 km² free limit
        self.fee_per_sq_meter = Decimal('2.0')  # $2 per square meter

    def calculate_fee(self, area_sq_meters):
        if area_sq_meters <= self.free_limit * 1_000_000:  # Convert km² to m²
            return Decimal('0.0')  # No fee for the first 1 km²
        else:
            return (area_sq_meters - (self.free_limit * 1_000_000)) * self.fee_per_sq_meter

    def process_payment(self, user_id, area_sq_meters):
        fee = self.calculate_fee(area_sq_meters)
        if fee > 0:
            # Here you would integrate with a payment gateway
            # For example, charge the user using their payment method
            return jsonify({"message": "Payment processed", "amount": str(fee)}), 200
        else:
            return jsonify({"message": "No payment required"}), 200

payment_service = PaymentService()