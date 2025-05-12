from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship
from database.base import Base

class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    area_size = Column(Float, nullable=False)
    total_cost = Column(Float, nullable=False)
    status = Column(String, default='pending')

    user = relationship("User", back_populates="orders")