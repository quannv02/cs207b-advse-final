# 1st: please learn about how to using git first

Basically everyone should work on there own branch and when they want to merge to the main, first merge the main into your branch first (then solve conflict if have) then you can merge your branch into master.


# 2nd setup environment:

I recommend everyone use anaconda, conda for sort to setup the environment
the python version for this system is `python3.9` for the UI, you can use any free-to-use library (for commercial or not)
  
All the requirement package are in the `requirement.txt` file  
  
To start develop the app just use command `python main.py`  
now the app should auto restart when ever you save the code   
incase you don't know how to exit the app press ctrl-c in terminal 


The app in real env normally using docker to deploy, you should learn about this for future advantage

# 3rd for developer

just remove `hotel.db` to reset the db :) and use `init.db` to create some draft inside 

Your recommend or notes go here or direct in code !!!, please use "TODO" key to easier found what need to implement later right when you remember it !!  
ex:   
TODO: write more here   


Here are some suggestions for what you could do next and how to write unit tests for them:

TODO: 
    Add more fields to the Room and Reservation models: Currently, the Room model only has fields for room_number and price, and the Reservation model only has fields for start_date, end_date, and room_id. Depending on the requirements of your hotel app, you may need to add more fields to these models, such as room_type, description, guest_capacity, checkin_time, checkout_time, etc.

    To test the new fields, you can create objects with different values for each field and test that the values are stored correctly in the database. For example, you could create a new Room object with a room number of "101", a price of 100, a room type of "Standard", and a guest capacity of 2, and then test that the object is stored correctly in the database.

TODO:
    Add more routes and views: Currently, the app only has a single view to display a list of rooms and a detail view to display a single room. Depending on the requirements of your hotel app, you may need to add more views and routes, such as a view to display a list of reservations, a view to allow guests to make reservations, a view to allow staff to manage reservations, etc.

    To test the new views and routes, you can use Flask's built-in testing client to simulate user interactions with the app. For example, you could write a test that simulates a guest making a reservation for a room, and then check that the reservation is stored correctly in the database and that the guest can see the reservation details.

TODO:
    Add authentication and authorization: Currently, the app does not have any authentication or authorization mechanisms in place, which means that anyone can access any part of the app. Depending on the requirements of your hotel app, you may need to add authentication and authorization to restrict access to certain views and routes, and to allow staff to manage reservations and room availability.

    To test the authentication and authorization mechanisms, you can write tests that simulate different types of users (e.g. guests, staff, managers) trying to access different parts of the app. For example, you could write a test that simulates a guest trying to access the staff-only reservation management page, and check that the guest is redirected to the login page.

TODO:
    Add error handling and validation: Currently, the app does not have any error handling or input validation mechanisms in place, which means that users can enter invalid data or cause errors by using the app incorrectly. Depending on the requirements of your hotel app, you may need to add error handling and input validation to ensure that the app behaves correctly and gracefully handles errors.

    To test the error handling and validation mechanisms, you can write tests that simulate different types of user errors (e.g. entering invalid dates, entering negative room prices) and check that the app responds correctly and displays informative error messages.

I hope these suggestions help! Good luck with your hotel app development.

