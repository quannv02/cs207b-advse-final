# models.py
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(20), unique=True, nullable=False)
    password = Column(String(128), nullable=False)
    friendly_name = Column(String(50), nullable=False)
    phone_number = Column(String(20), nullable=False)
    email = Column(String(50), nullable=False)
    is_admin = Column(Integer, nullable=False, default=0)
    is_staff = Column(Integer, nullable=False, default=0)

class Room(Base):
    __tablename__ = 'rooms'
    id = Column(Integer, primary_key=True)
    room_number = Column(String(50), nullable=False)
    price = Column(Float, nullable=False)
    floor = Column(String(10), nullable=False)
    capacity = Column(Integer, nullable=False, default=1)
    image = Column(String(50), nullable=False)
    description = Column(String(1000), nullable=False)
    available = Column(Integer, nullable=False, default=1) # 0 = not available, 1 = available
    average_rating = Column(Float, nullable=False, default=0)

class Reservation(Base):
    __tablename__ = 'reservations'
    id = Column(Integer, primary_key=True)
    room_id = Column(Integer, ForeignKey('rooms.id'), nullable=False)
    guest_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    start_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    end_date = Column(DateTime, nullable=False)
    room = relationship('Room', backref='reservations')

class Review(Base):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    room_id = Column(Integer, ForeignKey('rooms.id'), nullable=False)
    comment = Column(String(1000), nullable=False)
    rating = Column(Integer, nullable=False) # 1-5
    show = Column(Integer, nullable=False, default=0) # 0 = hidden, 1 = visible
    room = relationship('Room', backref='reviews')

engine = create_engine('sqlite:///hotel.db')
DBSession = sessionmaker(bind=engine)
Base.metadata.create_all(engine)