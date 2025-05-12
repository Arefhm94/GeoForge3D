from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..models.user import User
from ..utils.security import hash_password, verify_password
from ..database import get_db

router = APIRouter()

@router.post("/register")
def register_user(user: User, db: Session = Depends(get_db)):
    user.password = hash_password(user.password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": "User registered successfully"}

@router.post("/login")
def login_user(username: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return {"message": "Login successful", "user_id": user.id}