
# controllers.py
from model import Room, Reservation, DBSession, User
from sqlalchemy import create_engine
from werkzeug.security import generate_password_hash, check_password_hash

# def create_database():
#     engine = create_engine('sqlite:///hotel.db')
#     Base.metadata.create_all(engine)

# controllers.py
# from models import Room, Reservation, Session

def get_all_rooms():
    session = DBSession()
    rooms = session.query(Room).all()
    session.close()
    return rooms

def get_room_by_id(room_id):
    session = DBSession()
    room = session.query(Room).get(room_id)
    session.close()
    return room

def get_reservations_by_room_id(room_id):
    session = DBSession()
    reservations = session.query(Reservation).filter_by(room_id=room_id).all()
    session.close()
    return reservations

def add_room(room_number, price):
    session = DBSession()
    room = Room(room_number=room_number, price=price)
    session.add(room)
    session.commit()
    session.close()
    return room

def make_reservation(start_date, end_date, guest_name, room_id):
    session = DBSession()
    reservation = Reservation(start_date=start_date, end_date=end_date, guest_name=guest_name, room_id=room_id)
    session.add(reservation)
    session.commit()
    session.close()
    return reservation

def createUsers(username, password, friendly_name, phone_number, email, is_admin, is_staff):
    session = DBSession()
    hashed_password = generate_password_hash(password)
    user = User(username=username, password=hashed_password, friendly_name=friendly_name, phone_number=phone_number, email=email, is_admin=is_admin, is_staff=is_staff)
    session.add(user)
    session.commit()
    session.close()
    return user

def checkUserAuthenticate(username, password):
    session = DBSession()
    user = session.query(User).filter_by(username=username).first()
    session.close()
    if user:
        if check_password_hash(user.password, password):
            return True
        else:
            return False
    else:
        return False

def getUsers(username):
    session = DBSession()
    users = session.query(User).filter_by(username=username).first()
    session.close()
    return users
# def add_room(number, floor, capacity):
#     room = Room(number=number, floor=floor, capacity=capacity)
#     engine = create_engine('sqlite:///hotel.db')
#     # Base.metadata.create_all(engine)
#     with engine.begin() as connection:
#         connection.execute(f"INSERT INTO rooms (number, floor, capacity) VALUES ('{number}', {floor}, {capacity})")

# def make_reservation(room_id, guest_name, start_date, end_date):
#     reservation = Reservation(room_id=room_id, guest_name=guest_name, start_date=start_date, end_date=end_date)
#     engine = create_engine('sqlite:///hotel.db')
#     with engine.begin() as connection:
#         connection.execute(f"INSERT INTO reservations (room_id, guest_name, start_date, end_date) VALUES ({room_id}, '{guest_name}', '{start_date}', '{end_date}')")
