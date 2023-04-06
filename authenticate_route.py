from flask import Flask, jsonify, render_template, request, redirect, url_for, session, Blueprint
from controller import *
from app import app


authenticate_route = Blueprint('authenticate_route', __name__)

@authenticate_route.route('/signup', methods=['GET', 'POST'])
def signup():
    with app.app_context():
        if session.get('logged_in'):
            return redirect(url_for('index'))
        
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        friendly_name = request.form['friendly_name'] if "friendly_name" in request.form else username
        phone_number = request.form['phone_number'] if "phone_number" in request.form else ""
        email = request.form['email'] if "email" in request.form else ""

        if not username or not password:
            return render_template('login.html', error="Username and password are required", sigin = "", signup = "active")

        if getUser(username):
            return render_template('login.html', error="Username already exists", sigin = "", signup = "active")
        
        is_admin = 0
        is_staff = 0

        # TODO: bypass the admin and staff creation
        if username == "admin":
            is_admin = 1
        
        if username == "staff":
            is_staff = 1

        createUsers(username, password, friendly_name, phone_number, email, is_admin, is_staff)

        user = getUser(username)

        session['logged_in'] = True
        session['user'] = username
        session['friendly_name'] = user.friendly_name
        session['id'] = user.id
        session['is_admin'] = user.is_admin
        session['is_staff'] = user.is_staff
        return redirect(url_for('index'))
    return render_template('login.html', error="", signin = "", signup = "active")

@authenticate_route.route('/logout')
def logout():
    session['logged_in'] = False
    session.clear()
    return redirect(url_for('index'))

@authenticate_route.route('/login', methods=['GET', 'POST'])
def login():
    with app.app_context():
        if session.get('logged_in'):
            return redirect(url_for('index'))
        
    if request.method == 'POST':
        # try:
        username = request.form['username']
        password = request.form['password']
        # except:
        print(request.form)
        if not username or not password:
            return render_template('login.html', error="Username and password are required", sigin = "active", signup = "")


        if checkUserAuthenticate(username, password):
            user = getUser(username)
            session['logged_in'] = True
            session['user'] = username
            if user.friendly_name:
                session['friendly_name'] = user.friendly_name
            else:
                session['friendly_name'] = username
            session['id'] = user.id
            session['is_admin'] = user.is_admin
            session['is_staff'] = user.is_staff
            
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error="Username or password is incorrect", sigin = "active", signup = "")
    
    return render_template('login.html', error="", sigin = "active", signup = "")
