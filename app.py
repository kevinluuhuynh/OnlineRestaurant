from flask import Flask, render_template, request,redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re


app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'restaurant'
app.config['SECRET_KEY'] = 'c3f3d37c905ea800401f0659'

mysql = MySQL(app)


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route('/menu')
def menu_page():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM menu")
    data = cursor.fetchall()
    return render_template('menu.html', menu=data)


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'first_name' in request.form and 'last_name' in request.form and 'phone' in request.form and 'address' in request.form:
        # Create variables for easy access
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        phone = request.form['phone']
        address = request.form['address']

        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM account WHERE email = %s', (phone,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO account (first_name, password, email) VALUES ( %s, %s, %s)', (first_name, last_name, phone, address,))
            mysql.connection.commit()
            msg = 'You have successfully registered!'


    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)

if __name__ == '__main__':
    app.run(debug=True)