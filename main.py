# this also the views
from flask import Flask, render_template, request, redirect
from controller import add_room, get_all_rooms, get_room_by_id, get_reservations_by_room_id

app = Flask(__name__)

@app.route('/')
def index():
    rooms = get_all_rooms()
    
    return render_template('index.html', rooms=rooms)

@app.route('/rooms/<int:room_id>')
def room(room_id):
    room = get_room_by_id(room_id)
    reservations = get_reservations_by_room_id(room_id)
    return render_template('room.html', room=room, reservations=reservations)

@app.route('/add_room', methods=['POST'])
def add_room_view():
    room_number = request.form['room_number']
    price = request.form['price']
    add_room(room_number, price)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
