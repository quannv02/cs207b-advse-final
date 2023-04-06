
# controllers.py
from model import Room, Reservation, DBSession, User, Review
from sqlalchemy import create_engine
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

"""     room interaction    """ 

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

def add_room(room_number, price, floor, image, description, available, average_rating):
    session = DBSession()
    room = Room(room_number=room_number, price=price, floor=floor, image=image, description=description, available=available, average_rating=average_rating)
    session.add(room)
    session.commit()
    session.close()
    return room

# TODO: not used
def modify_room(room_id, room_number, price, floor,capacity, image, description, available, average_rating):
    session = DBSession()
    room = session.query(Room).get(room_id)
    room.room_number = room_number
    room.price = price
    room.floor = floor
    room.capacity = capacity
    room.image = image
    room.description = description
    room.available = available
    room.average_rating = average_rating
    session.commit()
    session.close()
    return room

def delete_room(room_id):
    session = DBSession()
    room = session.query(Room).get(room_id)
    session.delete(room)
    session.commit()
    session.close()
    return room

def get_available_rooms(start_date, end_date, number_adults, number_children, price):
    
    people = number_adults + int(number_children/2)
    session = DBSession()
    rooms = session.query(Room).filter_by(available=1).all()
    for room in rooms:
        reservations = session.query(Reservation).filter_by(room_id=room.id).all()
        for reservation in reservations:
            if reservation.start_date <= start_date and reservation.end_date >= end_date:
                rooms.remove(room)
            elif reservation.start_date <= start_date and reservation.end_date >= start_date:
                rooms.remove(room)
            elif reservation.start_date <= end_date and reservation.end_date >= end_date:
                rooms.remove(room)
            elif reservation.start_date >= start_date and reservation.end_date <= end_date:
                rooms.remove(room)
        # print(room.price, price)
        if room.price > price or room.capacity < people:
            # print("removed")
            rooms.remove(room)

    session.close()
    return rooms

# TODO: not used
def update_available_rooms():
    session = DBSession()
    rooms = session.query(Room).all()
    for room in rooms:
        reservations = session.query(Reservation).filter_by(room_id=room.id).all()
        for reservation in reservations:
            if reservation.start_date <= datetime.now() and reservation.end_date >= datetime.now():
                room.available = 0
                session.commit()
            elif reservation.end_date < datetime.now():
                room.available = 1
                session.commit()
    session.close()
    return rooms

# TODO: not used
def update_ratings():
    session = DBSession()
    rooms = session.query(Room).all()
    for room in rooms:
        reviews = session.query(Review).filter_by(room_id=room.id).all()
        if len(reviews) == 0:
            room.average_rating = 0
        else:
            total = 0
            for review in reviews:
                total += review.rating
            room.average_rating = total / len(reviews)
        session.commit()
    session.close()
    return rooms

"""    Reservation interaction   """

# TODO: not used
def get_all_reservations():
    session = DBSession()
    reservations = session.query(Reservation).all()
    session.close()
    return reservations

def get_reservations_by_guest_id(guest_id, status = 0):
    session = DBSession()
    if status == 0:
        reservations_raw = session.query(Reservation).filter_by(guest_id=guest_id, status=0).all()
    else:
        reservations_raw = session.query(Reservation).filter_by(guest_id=guest_id).all()
    
    reservations = []
    for reservation in reservations_raw:
        room = session.query(Room).get(reservation.room_id)
        reservation.room_number = room.room_number
        reservation.check_in = reservation.start_date.strftime("%d-%m-%Y")
        reservation.check_out = reservation.end_date.strftime("%d-%m-%Y")
        reservation.day_stay = reservation.end_date - reservation.start_date
        reservation.base_price = room.price
        reservation.price = room.price * reservation.day_stay.days
        reservation.floor = room.floor
        reservation.capacity = room.capacity
        reservation.image = room.image
        reservations.append(reservation)
    session.close()
    return reservations

def pay_reservations_by_guest_id(guest_id):
    session = DBSession()
    reservations = session.query(Reservation).filter_by(guest_id=guest_id).all()
    for reservation in reservations:
        reservation = session.query(Reservation).get(reservation.id)
        reservation.status = 1
        session.commit()
    session.close()
    return reservations

def get_reservations_by_room_id(room_id):
    session = DBSession()
    reservations_raw = session.query(Reservation).filter_by(room_id=room_id).all()
    reservations = []
    for reservation in reservations_raw:
        room = session.query(Room).get(reservation.room_id)
        reservation.room_number = room.room_number
        reservation.price = room.price
        reservation.floor = room.floor
        reservation.capacity = room.capacity
        reservation.image = room.image
        reservations.append(reservation)

    session.close()
    return reservations

def make_reservation(guest_id, room_id, start_date, end_date):
    session = DBSession()
    reservation = Reservation(start_date=start_date, end_date=end_date, guest_id=guest_id, room_id=room_id)
    
    reservations = session.query(Reservation).filter_by(room_id=room_id).all()
    for reservation in reservations:
        if reservation.start_date <= start_date and reservation.end_date >= end_date:
            return False
        elif reservation.start_date <= start_date and reservation.end_date >= start_date:
            return False
        elif reservation.start_date <= end_date and reservation.end_date >= end_date:
            return False
        elif reservation.start_date >= start_date and reservation.end_date <= end_date:
            return False
    
    session.add(reservation)
    session.commit()
    session.close()
    return True

def delete_reservation(reservation_id):
    session = DBSession()
    reservation = session.query(Reservation).get(reservation_id)
    session.delete(reservation)
    session.commit()
    session.close()
    return reservation

"""   Review interaction   """

def get_all_reviews():
    session = DBSession()
    reviews = session.query(Review).all()
    session.close()
    return reviews

def get_reviews_by_room_id(room_id):
    session = DBSession()
    reviews = session.query(Review).filter_by(room_id=room_id).all()
    review_with_name = []
    for review in reviews:
        user = session.query(User).get(review.user_id)
        review.name = user.username if user.friendly_name == "" else user.friendly_name
        review_with_name.append(review)

    session.close()
    return review_with_name

def add_review(room_id, user_id, comment, rating):
    session = DBSession()
    # check room_id
    room = session.query(Room).get(room_id)
    if room is None:
        return None
    # check user_id
    user = session.query(User).get(user_id)
    if user is None:
        return None

    comment = Review(room_id=room_id, user_id=user_id, comment=comment, rating=rating)
    session.add(comment)
    session.commit()
    session.close()
    return comment

"""  DONE:  User interaction """

def createUsers(username, password, friendly_name, phone_number, email, is_admin, is_staff):
    session = DBSession()
    hashed_password = generate_password_hash(password)
    user = User(username=username, password=hashed_password, friendly_name=friendly_name, phone_number=phone_number, email=email, is_admin=is_admin, is_staff=is_staff)
    session.add(user)
    session.commit()
    session.close()
    return user

def modifyUser(id, username, password, friendly_name, phone_number, email, is_admin, is_staff):
    session = DBSession()
    
    user = session.query(User).get(id)

    if not user:
        return None
    
    user.username = username
    user.friendly_name = friendly_name
    user.phone_number = phone_number
    user.email = email
    user.is_admin = is_admin
    user.is_staff = is_staff

    if password:
        hashed_password = generate_password_hash(password)
        user.password = hashed_password
    
    session.add(user)
    session.commit()
    session.close()
    return user

def deleteUser(id):
    session = DBSession()
    user = session.query(User).get(id)
    session.delete(user)
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

def getUser(username = None, id = None):
    if id:
        session = DBSession()
        user = session.query(User).get(id)
        session.close()
        return user
    session = DBSession()
    user = session.query(User).filter_by(username=username).first()
    session.close()
    return user

def getAllUsers():
    session = DBSession()
    users = session.query(User).all()
    session.close()
    return users