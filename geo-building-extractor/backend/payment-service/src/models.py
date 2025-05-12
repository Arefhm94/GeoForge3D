from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Payment(Base):
    __tablename__ = 'payments'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    amount = Column(Float, nullable=False)
    status = Column(String, nullable=False)
    created_at = Column(String, nullable=False)  # Consider using DateTime for better handling
    updated_at = Column(String, nullable=False)  # Consider using DateTime for better handling

class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    area_size = Column(Float, nullable=False)
    total_cost = Column(Float, nullable=False)
    payment_id = Column(Integer, nullable=True)  # Foreign key to Payment table
    created_at = Column(String, nullable=False)  # Consider using DateTime for better handling
    updated_at = Column(String, nullable=False)  # Consider using DateTime for better handling