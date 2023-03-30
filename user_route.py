from controller import *
from flask import jsonify, render_template, request, redirect, url_for, session, Blueprint
from app import app

user_route = Blueprint('user_route', __name__)


@user_route.route('/room/<int:room_id>', methods=['GET'])
def room(room_id):
    with app.app_context():
        if not session.get('logged_in'):
            return redirect(url_for('authenticate_route.login'))
        else:
            room = get_room_by_id(room_id)
            reviews = get_reviews_by_room_id(room_id)
            message = request.args.get('message')
            error = request.args.get('error')
            return render_template('user_room.html', room=room, reviews=reviews, message=message, error=error)

@user_route.route('/reserves', methods=['GET'])
def reserves():
    with app.app_context():
        if not session.get('logged_in'):
            return redirect(url_for('authenticate_route.login'))
        else:
            user_id = session['id']
            reservations = get_reservations_by_guest_id(user_id)
            message = request.args.get('message')
            error = request.args.get('error')
            return render_template('user_reserves.html', reservations=reservations, message=message, error=error)

@user_route.route('/cancel_reservation/<int:reservation_id>', methods=['GET'])
def cancel_reservation(reservation_id):
    with app.app_context():
        if not session.get('logged_in'):
            return redirect(url_for('authenticate_route.login'))
        else:
            user_id = session['id']
            #TODO: implement this
            # cancel_reservation(reservation_id)
            return redirect(url_for('user_route.reserves', error = "Not implemented yet"))
        

@user_route.route('/payment/<int:reservation_id>', methods=['GET'])
def payment(reservation_id):
    with app.app_context():
        if not session.get('logged_in'):
            return redirect(url_for('authenticate_route.login'))
        else:
            # reservation = get_reservation_by_id(reservation_id)
            # return render_template('user_payment.html', reservation=reservation)
            return redirect(url_for('user_route.reserves'))

@user_route.route('/reserve/<int:room_id>', methods=['POST'])
def reserve(room_id):
    with app.app_context():
        if not session.get('logged_in'):
            return redirect(url_for('authenticate_route.login'))
        else:
            user_id = session['id']
            start_date = datetime.datetime.strptime(request.form['start_date'], '%Y-%m-%d')
            end_date = datetime.datetime.strptime(request.form['end_date'], '%Y-%m-%d')
            make_reservation(user_id, room_id, start_date, end_date)
            return redirect(url_for('user_route.room', room_id=room_id))


@user_route.route('/add_review_route/<int:room_id>', methods=['POST'])
def add_review_route(room_id):
    with app.app_context():
        if not session.get('logged_in'):
            return redirect(url_for('authenticate_route.login'))
        else:
            user_id = session['id']
            rating = request.form['rating']
            comment = request.form['comment']
            add_review(room_id,user_id, comment, rating)
            return redirect(url_for('user_route.room', room_id=room_id, message="Review added successfully"))