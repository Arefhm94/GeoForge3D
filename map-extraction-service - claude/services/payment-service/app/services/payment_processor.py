from fastapi import HTTPException
from pydantic import BaseModel
import stripe

# Initialize Stripe with your secret key
stripe.api_key = "your_stripe_secret_key"

class PaymentRequest(BaseModel):
    user_id: str
    amount: float
    currency: str = "usd"

class PaymentResponse(BaseModel):
    success: bool
    message: str
    charge_id: str = None

async def process_payment(payment_request: PaymentRequest) -> PaymentResponse:
    try:
        # Create a charge using Stripe
        charge = stripe.Charge.create(
            amount=int(payment_request.amount * 100),  # Amount in cents
            currency=payment_request.currency,
            description=f"Payment for user {payment_request.user_id}",
            metadata={"user_id": payment_request.user_id},
        )
        return PaymentResponse(success=True, message="Payment successful", charge_id=charge.id)
    except stripe.error.StripeError as e:
        raise HTTPException(status_code=400, detail=str(e.user_message))
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while processing the payment")