
# example how to use the database and model 
from controller import *
from model import *
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
# if __name__ == '__main__':
#     #TODO: create_database() and run unit tets

#     # insert 12 room 
#     for i in range(12):
#         print(add_room(i, i**2) )
#     # print(get_all_rooms())
#     room_ids = [room.id for room in get_all_rooms()]

#     print(room_ids)

#     make_reservation(datetime.fromisoformat('2019-12-04'), \
#     datetime.fromisoformat('2020-12-04'),'John Doe', room_ids[0])

if __name__ == '__main__':
    import unittest

    class TestDatabase(unittest.TestCase):
        def testCreateUsers(self):
            self.engine = create_engine('sqlite:///:memory:')
            self.session = sessionmaker(bind=self.engine)
            Base.metadata.create_all(self.engine)

            user = createUsers("test", "test", "test", "test", "test", False, False,self.session())
            user = getUser(username="test", session=self.session())
            self.assertEqual(user.username, "test")
            self.assertEqual(user.friendly_name, "test")
            self.assertEqual(user.phone_number, "test")
            self.assertEqual(user.email, "test")
            self.assertEqual(user.is_admin, False)
            self.assertEqual(user.is_staff, False)

            deleteUser(user.id,session = self.session())
            

        def testModifyUser(self):
            self.engine = create_engine('sqlite:///:memory:')
            self.session = sessionmaker(bind=self.engine)
            Base.metadata.create_all(self.engine)
        
            user = createUsers("te", "tt", "tst", "est", "tst", True, True,session=self.session())
            user = getUser(username="te",  session=self.session())
            modifyUser(user.id, "test", "test", "test", "test", "test", False, False, session=self.session())
            user = getUser(id=user.id, session=self.session())
            self.assertEqual(user.username, "test")
            self.assertEqual(user.friendly_name, "test")
            self.assertEqual(user.phone_number, "test")
            self.assertEqual(user.email, "test")
            self.assertEqual(user.is_admin, False)
            self.assertEqual(user.is_staff, False)
            deleteUser(user.id, session=self.session())

    unittest.main()