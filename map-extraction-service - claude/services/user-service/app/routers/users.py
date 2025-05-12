from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..models.user import User
from ..utils.security import get_password_hash, verify_password
from ..database import get_db

router = APIRouter()

@router.post("/register")
def register_user(user: User, db: Session = Depends(get_db)):
    user.password = get_password_hash(user.password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.post("/login")
def login_user(username: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return {"message": "Login successful", "user_id": user.id}

@router.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user