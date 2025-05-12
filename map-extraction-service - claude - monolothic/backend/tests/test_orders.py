from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.orders.models import Order
from app.auth.dependencies import get_current_user

router = APIRouter()

@router.post("/orders/")
def create_order(order: Order, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    db.add(order)
    db.commit()
    db.refresh(order)
    return order

@router.get("/orders/{order_id}")
def read_order(order_id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    order = db.query(Order).filter(Order.id == order_id, Order.user_id == current_user.id).first()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.get("/orders/")
def read_orders(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    orders = db.query(Order).filter(Order.user_id == current_user.id).offset(skip).limit(limit).all()
    return orders

@router.delete("/orders/{order_id}")
def delete_order(order_id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    order = db.query(Order).filter(Order.id == order_id, Order.user_id == current_user.id).first()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    db.delete(order)
    db.commit()
    return {"detail": "Order deleted"}