from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    balance = Column(Float, default=0.0)  # To manage user balance for payments
    created_at = Column(Integer)  # Timestamp for account creation

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, email={self.email})>"