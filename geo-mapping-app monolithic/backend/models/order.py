from datetime import datetime
from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from . import Base

class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    area_size = Column(Float, nullable=False)  # in square meters
    cost = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="orders")

    def __init__(self, user_id, area_size):
        self.user_id = user_id
        self.area_size = area_size
        self.cost = self.calculate_cost()

    def calculate_cost(self):
        if self.area_size <= 1000000:  # 1 km² in square meters
            return 0.0
        else:
            return (self.area_size - 1000000) * 2.0  # $2 per square meter after the first km²

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'area_size': self.area_size,
            'cost': self.cost,
            'created_at': self.created_at.isoformat()
        }