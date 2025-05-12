from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from backend.common.database import Base

class Rectangle(Base):
    __tablename__ = 'rectangles'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    min_latitude = Column(Float, nullable=False)
    max_latitude = Column(Float, nullable=False)
    min_longitude = Column(Float, nullable=False)
    max_longitude = Column(Float, nullable=False)
    area = Column(Float, nullable=False)

    user = relationship("User", back_populates="rectangles")

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)

    rectangles = relationship("Rectangle", back_populates="user")