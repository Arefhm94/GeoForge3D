from sqlalchemy import create_engine, Column, Integer, String, Float, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./test.db"  # Update with your database URL

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    created_at = Column(Float)

class Order(Base):
    __tablename__ = 'orders'
    
    id = Column(Integer, Sequence('order_id_seq'), primary_key=True)
    user_id = Column(Integer)
    area = Column(Float)
    price = Column(Float)
    created_at = Column(Float)

Base.metadata.create_all(bind=engine)