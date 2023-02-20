# models.py
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Room(Base):
    __tablename__ = 'rooms'

    id = Column(Integer, primary_key=True)
    room_number = Column(String(50), nullable=False)
    price = Column(Float, nullable=False)

class Reservation(Base):
    __tablename__ = 'reservations'

    id = Column(Integer, primary_key=True)
    start_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    end_date = Column(DateTime, nullable=False)
    guest_name = Column(String(50), nullable=False)
    room_id = Column(Integer, ForeignKey('rooms.id'), nullable=False)
    room = relationship('Room', backref='reservations')

engine = create_engine('sqlite:///hotel.db')
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)