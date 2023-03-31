# this also the views
from flask import Flask, render_template, request, redirect, session, url_for
from controller import getUser, add_room, get_all_rooms, get_room_by_id, get_reservations_by_room_id, getAllUsers, modifyUser

from authenticate_route import authenticate_route, app
from admin_route import admin_route
from user_route import user_route

app.register_blueprint(authenticate_route)
app.register_blueprint(admin_route)
app.register_blueprint(user_route)

@app.route('/')
def index():
    with app.app_context():
        if not session.get('logged_in'):
            return render_template('index.html')
        else:
            if session['is_admin']:
                users = getAllUsers()
                rooms = get_all_rooms()
                return render_template('admin.html', users=users ,rooms=rooms)
            
            if session['is_staff']:
                rooms = get_all_rooms()
                return render_template('staff.html',rooms=rooms)

            rooms = get_all_rooms()
            return render_template('user.html', rooms=rooms)



if __name__ == '__main__':
    app.run(debug=True)
