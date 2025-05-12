from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from .models import Order, OrderCreate
from ..auth.dependencies import get_current_user

router = APIRouter()

@router.post("/", response_model=Order)
def create_order(order: OrderCreate, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    db_order = Order(**order.dict(), user_id=current_user.id)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

@router.get("/{order_id}", response_model=Order)
def read_order(order_id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    order = db.query(Order).filter(Order.id == order_id, Order.user_id == current_user.id).first()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.get("/", response_model=list[Order])
def read_orders(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    orders = db.query(Order).filter(Order.user_id == current_user.id).offset(skip).limit(limit).all()
    return orders