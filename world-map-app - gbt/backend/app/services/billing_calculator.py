from decimal import Decimal

class BillingCalculator:
    def __init__(self):
        self.free_area_limit = Decimal('1.0')  # 1 km² in square kilometers
        self.fee_per_square_meter = Decimal('2.0')  # $2 per square meter

    def calculate_billing(self, area_in_square_km):
        if area_in_square_km <= self.free_area_limit:
            return Decimal('0.0')  # No charge for the first 1 km²
        else:
            area_in_square_meters = (area_in_square_km - self.free_area_limit) * 1_000_000  # Convert km² to m²
            return area_in_square_meters * self.fee_per_square_meter

    def get_fee(self, area_in_square_km):
        total_fee = self.calculate_billing(area_in_square_km)
        return total_fee.quantize(Decimal('0.01'))  # Round to two decimal places for currency representation