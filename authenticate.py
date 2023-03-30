from flask import Flask, jsonify, render_template, request, redirect, url_for, session, Blueprint

from controller import *

app = Flask(__name__)

# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

authenticate_route = Blueprint('', __name__)

@authenticate_route.route('/signup', methods=['GET', 'POST'])
def signup():
    with app.app_context():
        if session.get('logged_in'):
            return redirect(url_for('index'))
        
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            return render_template('login.html', error="Username and password are required", sigin = "", signup = "active")

        
        if getUsers(username):
            return render_template('login.html', error="Username already exists", sigin = "", signup = "active")
        
        createUsers(username, password, "", "", "", False, False)

        user = getUsers(username)

        print(user)

        session['logged_in'] = True
        session['user'] = username
        session['id'] = user.id

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

        user = getUsers(username)

        if checkUserAuthenticate(username, password):
            session['logged_in'] = True
            session['user'] = username
            session['id'] = user.id
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error="Username or password is incorrect", sigin = "active", signup = "")
    return render_template('login.html', error="", sigin = "active", signup = "")
