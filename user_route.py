from controller import *
from flask import jsonify, render_template, request, redirect, url_for, session, Blueprint
from app import app

user_route = Blueprint('user_route', __name__)

@user_route.route('/user', methods=['GET'])
def user():
    with app.app_context():
        if not session.get('logged_in'):
            return redirect(url_for('authenticate_route.login'))
        else:
            user_id = session['id']
            message = request.args.get('message')
            error = request.args.get('error')
            return render_template('user.html',  message=message, error=error)


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
            request_pay = False
            for reservation in reservations:
                if reservation.status == 0:
                    request_pay = True
                    break

            return render_template('user_reserves.html', reservations=reservations, request_pay= request_pay, message=message, error=error)

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
        

@user_route.route('/payment/', methods=['GET'])
def payment():
    with app.app_context():
        if not session.get('logged_in'):
            return redirect(url_for('authenticate_route.login'))
        else:
            user_id = session['id']
            reservations = get_reservations_by_guest_id(user_id)
            message = request.args.get('message')
            error = request.args.get('error')
            request_pay = False
            total_pay = 0
            finally_pay = 0
            
            for reservation in reservations:
                if reservation.status == 0:
                    request_pay = True
                    total_pay += reservation.price

            if not request_pay:
                return redirect(url_for('user_route.reserves', error = "No pending reservations"))
            
            tax = round(total_pay * 0.1,1)
            finally_pay = total_pay + tax

            return render_template('user_payment.html', reservation=reservations, message=message, error=error, 
                                   request_pay=request_pay, total_pay=total_pay, tax=tax, finally_pay=finally_pay)
            # return redirect(url_for('user_route.reserves'))

@user_route.route('/payment_accept', methods=['GET'])
def payment_accept():
    with app.app_context():
        if not session.get('logged_in'):
            return redirect(url_for('authenticate_route.login'))
        else:
            user_id = session['id']
            reservations = get_reservations_by_guest_id(user_id)
            message = request.args.get('message')
            error = request.args.get('error')
            request_pay = False
            total_pay = 0
            finally_pay = 0
            
            for reservation in reservations:
                if reservation.status == 0:
                    request_pay = True
                    total_pay += reservation.price
                    
            if not request_pay:
                return redirect(url_for('user_route.reserves', error = "No pending reservations"))
            
            tax = round(total_pay * 0.1,1)
            finally_pay = total_pay + tax

            return render_template('user_payment_accept.html', reservation=reservations, message=message, error=error, 
                                   request_pay=request_pay, total_pay=total_pay, tax=tax, finally_pay=finally_pay)
            # return redirect(url_for('user_route.reserves'))


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
            return redirect(url_for('user_route.reserves', room_id=room_id))


@user_route.route('/add_review_route/<int:room_id>', methods=['POST'])
def add_review_route(room_id):
    with app.app_context():
        if not session.get('logged_in'):
            return redirect(url_for('authenticate_route.login'))
        else:
            user_id = session['id']
            rating = request.form['rating'] if 'rating' in request.form else '999'
            comment = request.form['comment']
            add_review(room_id,user_id, comment, rating)
            if session['is_admin'] or session['is_staff']:
                return redirect(url_for('admin_route.modify_room', room_id=room_id, message="Review added successfully"))
            else:
                return redirect(url_for('user_route.room', room_id=room_id, message="Review added successfully"))