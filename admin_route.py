from flask import jsonify, render_template, request, redirect, url_for, session, Blueprint
from controller import *
from app import app

admin_route = Blueprint('admin_route', __name__)
        
@admin_route.route('/users/<int:user_id>')
def users(user_id):
    with app.app_context():
        if session.get('logged_in'):
            if session['is_admin'] or session['id'] == user_id:
                user = getUser(id = user_id)
                return render_template('admin_modify_user.html', user=user)
        return redirect(url_for('index'))

@admin_route.route('/modify_user/<int:user_id>', methods=['GET', 'POST'])
def modify_user(user_id):
    with app.app_context():
        if session.get('logged_in'):
            if session['is_admin'] or session['id'] == user_id:
                print(request.form)
                if request.method == 'POST':
                    #TODO: not remove admin
                    username = request.form['username'] if 'username' in request.form else None
                    password = request.form['password'] if 'password' in request.form else None
                    if password == "*****":
                        password = None
                    friendly_name = request.form['friendly_name'] if 'friendly_name' in request.form else ''
                    phone_number = request.form['phone_number'] if 'phone_number' in request.form else ''
                    email = request.form['email'] if 'email' in request.form else ''
                    is_admin = request.form['is_admin'] if 'is_admin' in request.form else False
                    is_staff = request.form['is_staff'] if 'is_staff' in request.form else False
                    
                    if not username:
                        user = getUser(id = user_id)
                        return render_template('admin_modify_user.html',user=user, error="Username is required")

                    if not modifyUser(user_id, username, password, friendly_name, phone_number, email, is_admin, is_staff):
                        return render_template('admin_modify_user.html', error="User does not exist")
                
        return redirect(url_for('index'))
    
@admin_route.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    with app.app_context():
        if session.get('logged_in'):
            if session['is_admin']:
                #TODO: not remove admin
                if deleteUser(user_id):
                    return redirect(url_for('index'))
                return render_template('admin.html', error="User does not exist")
        return redirect(url_for('index'))

@admin_route.route('/add_room', methods=['POST'])
def add_room_view():
    with app.app_context():
        if not session.get('logged_in') or not session['is_admin']:
            return redirect(url_for('authenticate_route.login'))
        else:
            if 'room_number' not in request.form or 'price' not in request.form:
                return render_template('admin.html', error="Room number and price are required")
            room_number = request.form['room_number'] 
            price = request.form['price'] 
            floor = request.form['floor'] if 'floor' in request.form else "0"
            image = request.form['image'] if 'image' in request.form else "default.jpg"
            description = request.form['description'] if 'description' in request.form else "very nice room"
            available = request.form['available'] if 'available' in request.form else 1
            average_rating = request.form['average_rating'] if 'average_rating' in request.form else 5

            add_room(room_number, price, floor, image, description, available, average_rating)
            return redirect('/')

@admin_route.route('/modify_room/<int:room_id>', methods=['GET', 'POST'])
def modify_room_route(room_id):
    with app.app_context():
        if not session.get('logged_in'):
            return redirect(url_for('authenticate_route.login'))
        else:
            if request.method == 'POST' and (session['is_admin'] or session['is_staff']):
                if 'room_number' not in request.form or 'price' not in request.form:
                    return render_template('admin.html', error="Room number and price are required")
                room_number = request.form['room_number']
                price = request.form['price']
                floor = request.form['floor'] if 'floor' in request.form else "0"
                capacity = request.form['capacity'] if 'capacity' in request.form else 1
                image = request.form['image'] if 'image' in request.form else "default.jpg"
                description = request.form['description'] if 'description' in request.form else "very nice room"
                available = request.form['available'] if 'available' in request.form else 1
                average_rating = request.form['average_rating'] if 'average_rating' in request.form else 5
                # TODO: boundary check
                if modify_room(room_id, room_number, price, floor,capacity, image, description, available, average_rating):
                    return redirect('/')
                return redirect('/')
            else:
                room = get_room_by_id(room_id)
                reservations = get_reservations_by_room_id(room_id)
                reviews = get_reviews_by_room_id(room_id)
                return render_template('admin_staff_modify_room.html',reviews=reviews, room=room, reservations=reservations)

@admin_route.route('/delete_room/<int:room_id>', methods=['POST'])
def delete_room(room_id):
    with app.app_context():
        if not session.get('logged_in') or not session['is_admin']:
            return redirect(url_for('authenticate_route.login'))
        else:
            delete_room(room_id)
            return redirect('/')