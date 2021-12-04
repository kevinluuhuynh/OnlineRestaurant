from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, HiddenField, SelectField, RadioField
import random

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'restaurant'
app.config['SECRET_KEY'] = 'c3f3d37c905ea800401f0659'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///checkout.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = True

mysql = MySQL(app)
db = SQLAlchemy(app)

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


class MenuItem(db.Model):
    menu_id = db.Column(db.Integer, primary_key=True)
    dish_name = db.Column(db.String(50))
    price = db.Column(db.Integer)
    size = db.Column(db.String(20))
    description = db.Column(db.String(500))
    category = db.Column(db.String(100))


class AddMenuItem(FlaskForm):
    dish_name = StringField('DishName')
    price = IntegerField('Price')
    size = StringField('Size')
    description = TextAreaField('Description')
    category = StringField('Category')


class RemoveMenuItem(FlaskForm):
    dish_name = StringField('DishName')


class AddToCart(FlaskForm):
    quantity = IntegerField('Quantity')
    menu_id = HiddenField('ID')
    size = RadioField("Size", default= 'option1', choices=[('option1', "Small"), ('option1', "Large")])


class Order(db.Model):
    order_id = db.Column(db.Integer, primary_key=True)
    order_reference = db.Column(db.String(5))
    order_firstname = db.Column(db.String(20))
    order_lastname = db.Column(db.String(20))
    order_phone = db.Column(db.Integer)
    order_email = db.Column(db.String(50))
    order_address = db.Column(db.String(100))
    order_city = db.Column(db.String(100))
    order_zip = db.Column(db.String(20))
    order_status = db.Column(db.String(10))
    order_items = db.relationship('Order_Item', backref='order', lazy=True)


class Order_Item(db.Model):
    order_item_id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.order_id'))
    menu_id = db.Column(db.Integer, db.ForeignKey('menu_item.menu_id'))
    quantity = db.Column(db.Integer)


class Checkout(FlaskForm):
    chk_firstname = StringField('First Name')
    chk_lastname = StringField('LastName')
    chk_phone = StringField('Phone Number')
    chk_email = StringField('Email')
    chk_address = StringField('Address')
    chk_city = StringField('City')
    chk_zip = StringField('Zip Code')
    chk_cc_number = StringField('Credit Card Number')
    chk_cc_code = StringField('Security Code')
    chk_cc_exp = StringField('Expiration Date (mmyy)')
    chk_cc_name = StringField('Name on Card')
    chk_cc_zip = StringField('Billing Zip Code')


def handle_cart():
    menu_items = []
    grand_total = 0
    index = 0
    quantity_total = 0

    for dish in session['cart']:
        menu_item = MenuItem.query.filter_by(menu_id=dish['menu_id']).first()

        quantity = int(dish['quantity'])
        total = quantity * menu_item.price
        grand_total += total

        quantity_total += quantity

        menu_items.append({'menu_id': menu_item.menu_id, 'dish': menu_item.dish_name, 'price': menu_item.price,
                         'quantity': quantity, 'total': total, 'index': index})
        index += 1

    grand_total_plus_tax = grand_total * 1.07

    return menu_items, grand_total, grand_total_plus_tax, quantity_total


@app.route('/')
@app.route('/home')
def home_page():
    # Check if user is loggedin
    if 'loggedin' in session:
        return render_template('home.html', name=session['name'])
    return render_template('home.html')


@app.route('/menu')
def menu_page():
    menu = MenuItem.query.all()

    return render_template('menu.html', menu=menu)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        # Create variables for easy access
        email = request.form['email']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM account WHERE email = %s AND password = %s', (email, password,))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['account_id']
            session['email'] = account['email']
            session['name'] = account['first_name']
            # Redirect to home page
            return redirect(url_for('home_page'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    return render_template('login.html', msg=msg)


@app.route('/logout')
def logout_page():
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('email', None)
    session.pop('name', None)
    # Redirect to login page
    return redirect(url_for('login_page'))


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'first_name' in request.form and 'last_name' in request.form \
            and 'phone' in request.form and 'address' in request.form \
            and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        phone = request.form['phone']
        address = request.form['address']
        password = request.form['password']
        email = request.form['email']

        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM account WHERE email = % s', (email,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z]+', first_name):
            msg = 'First name must contain only characters!'
        elif not re.match(r'[A-Za-z]+', last_name):
            msg = 'Last name must contain only characters!'
        elif not re.match(r'[0-9]+', phone):
            msg = 'Phone number must contain only numbers!'
        elif not re.match(r'[A-Za-z0-9]+', first_name):
            msg = 'Address must contain only characters and numbers!'
        elif not first_name or not last_name or not phone or not address or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO account (first_name, last_name, phone, address, password, email)'
                           ' VALUES ( %s, %s, %s, %s, %s, %s)',
                           (first_name, last_name, phone, address, password, email,))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
            return redirect(url_for('login_page', msg=msg))

    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)


@app.route('/admin')
def admin():
    menu_items = MenuItem.query.all()

    return render_template('admin/index.html', admin=True, menu_items=menu_items)


@app.route('/admin/add', methods=['GET', 'POST'])
def add():
    form = AddMenuItem()

    if form.validate_on_submit():
        new_dish = MenuItem(dish_name=form.dish_name.data, price=form.price.data, size=form.size.data, description=form.description.data, category=form.category.data)

        db.session.add(new_dish)
        db.session.commit()

        return redirect(url_for('admin'))

    return render_template('admin/add-product.html', admin=True, form=form)


@app.route('/admin/remove', methods=['GET', 'POST'])
def remove():
    form = RemoveMenuItem()

    if form.validate_on_submit():
        removed_dish = form.dish_name.data

        MenuItem.query.filter(MenuItem.dish_name==removed_dish).delete()
        db.session.commit()

        return redirect(url_for('admin'))

    return render_template('admin/remove-product.html', admin=True, form=form)


@app.route('/add-to-cart', methods=['POST'])
def add_to_cart():
    if 'cart' not in session:
        session['cart'] = []

    form = AddToCart()
    if form.validate_on_submit():
        session['cart'].append({'menu_id' : form.menu_id.data, 'quantity' : form.quantity.data})
        session.modified = True
    print(session['cart'])
    return redirect(url_for('order_page'))


@app.route('/cart')
def cart():
    menu_items = []
    grand_total = 0
    index = 0

    for item in session['cart']:
        menu_item = MenuItem.query.filter_by(menu_id=item['menu_id']).first()

        quantity = int(item['quantity'])
        total = quantity * menu_item.price
        grand_total += total

        menu_items.append({'menu_id': menu_item.menu_id, 'dish_name': menu_item.dish_name, 'price': menu_item.price,
                         'quantity': quantity, 'total': total, 'index': index})
        index += 1

    grand_total_plus_tax = grand_total * 1.07

    return render_template('cart.html', menu_items=menu_items, grand_total=grand_total,
                           grand_total_plus_tax=grand_total_plus_tax)


@app.route('/remove-from-cart/<index>')
def remove_from_cart(index):
    del session['cart'][int(index)]
    session.modified = True
    return redirect(url_for('cart'))


@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    form = Checkout()

    menu_items, grand_total, grand_total_plus_tax, quantity_total = handle_cart()

    if form.validate_on_submit():

        order = Order()
        form.populate_obj(order)
        order.reference = ''.join([random.choice('ABCDE') for _ in range(5)])
        order.status = 'PENDING'

        for menu_item in menu_items:
            order_item = Order_Item(quantity=menu_item['quantity'], menu_id=menu_item['menu_id'])
            order.order_items.append(order_item)

        db.session.add(order)
        db.session.commit()

        session['cart'] = []
        session.modified = True

        return redirect(url_for('thankyou_page'))

    return render_template('checkout.html', form=form, grand_total=grand_total,
                           grand_total_plus_tax=grand_total_plus_tax, quantity_total=quantity_total)


@app.route('/order', methods=['GET', 'POST'])
def order_page():
    form = AddToCart()
    menu = MenuItem.query.all()
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM menu")
    data = cursor.fetchall()
    return render_template('order.html', data=data, menu=menu, form=form)


@app.route('/thankyou', methods=['GET', 'POST'])
def thankyou_page():
    return render_template('thankyou.html')


if __name__ == '__main__':
    app.run(debug=True)