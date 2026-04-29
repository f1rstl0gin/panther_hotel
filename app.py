#importing required materials
from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "secrretkey"

#function to connect to databse
def connect_database():
    conn = sqlite3.connect('hotel.db')
    conn.row_factory = sqlite3.Row
    return conn

#makes a table to store reservations
def make_table():
    conn = connect_database()
    conn.execute('''
        create table if not exists reservation (
            id integer primary key autoincrement,
            name text,
            checkin_date text,
            checkout_date text,
            room_type text
            )
    ''')
    conn.commit()
    conn.close()

#homepage backend
@app.route('/')
def index():
    return render_template('index.html')

#backend for reservation page
@app.route('/reserve', methods=['GET', 'POST'])
#function to reserve a room or view reservation page
def reserve():
    if request.method == 'POST':
        name = request.form['name']
        checkin_date = request.form['checkin_date']
        checkout_date = request.form['checkout_date']
        room_type = request.form['room_type']

        #saves information to session to use for confirmation
        session['name'] = name
        session['checkin_date'] = checkin_date
        session['checkout_date'] = checkout_date
        session['room_type'] = room_type

        #inserts reservation into hotel database
        conn = connect_database()
        conn.execute(
            'insert into reservation (name, checkin_date, checkout_date, room_type) values (?, ?, ?, ?)',
            (name, checkin_date, checkout_date, room_type)
        )
        conn.commit()
        conn.close()
        #takes user to confirmation page
        return redirect ('/confirmation')

    #shows user reservation page
    return render_template('reservation.html')

#confirmation page backend
@app.route('/confirmation')
def confirmation():
    #reads information from the session
    name = session.get('name')
    checkin_date = session.get('checkin_date')
    checkout_date = session.get('checkout_date')
    room_type = session.get('room_type')

    #allows my template to use stored name, date, etc info
    return render_template('confirmation.html',
    name = name,
    checkin_date = checkin_date,
    checkout_date = checkout_date,
    room_type = room_type
    
    )

#manager backend
@app.route('/manager')
#function to display reservations
def manager():
    conn = connect_database()
    reservations = conn.execute('select * from reservation').fetchall()
    conn.close
    return render_template('manager.html', reservations=reservations)

if __name__ == '__main__':
    make_table()
    app.run(debug = True)