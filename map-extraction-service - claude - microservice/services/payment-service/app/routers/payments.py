from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.payment_processor import process_payment

router = APIRouter()

class PaymentRequest(BaseModel):
    user_id: int
    amount: float
    description: str

@router.post("/payments/")
async def create_payment(payment_request: PaymentRequest):
    if payment_request.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be greater than zero.")
    
    payment_result = await process_payment(payment_request.user_id, payment_request.amount, payment_request.description)
    
    if not payment_result:
        raise HTTPException(status_code=500, detail="Payment processing failed.")
    
    return {"message": "Payment processed successfully", "payment_id": payment_result}