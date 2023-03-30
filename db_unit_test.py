
# example how to use the database and model 
from controller import add_room, get_all_rooms, make_reservation
from datetime import datetime

if __name__ == '__main__':
    #TODO: create_database() and run unit tets

    # insert 12 room 
    for i in range(12):
        print(add_room(i, i**2) )
    # print(get_all_rooms())
    room_ids = [room.id for room in get_all_rooms()]

    print(room_ids)

    make_reservation(datetime.fromisoformat('2019-12-04'), \
    datetime.fromisoformat('2020-12-04'),'John Doe', room_ids[0])
