from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

class BillingRequest(BaseModel):
    user_id: int
    area: float  # in square meters

class BillingResponse(BaseModel):
    total_cost: float
    message: str

@router.post("/billing/calculate", response_model=BillingResponse)
async def calculate_billing(request: BillingRequest):
    free_area_limit = 1000000  # 1 km² in square meters
    cost_per_square_meter = 2.0  # $2 per square meter

    if request.area <= 0:
        raise HTTPException(status_code=400, detail="Area must be greater than zero.")

    if request.area <= free_area_limit:
        total_cost = 0.0
        message = "First 1 km² of data extracted is free."
    else:
        total_cost = (request.area - free_area_limit) * cost_per_square_meter
        message = f"Total cost for {request.area - free_area_limit} square meters is ${total_cost}."

    return BillingResponse(total_cost=total_cost, message=message)