from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, HiddenField
from flask_wtf.file import FileField, FileAllowed

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
    dish_name = db.Column(db.String(50), unique=True)
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


class AddToCart(FlaskForm):
    quantity = IntegerField('Quantity')
    menu_id = HiddenField('ID')


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
"""def menu_page():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM menu")
    data = cursor.fetchall()
    return render_template('menu.html', menu=data)"""



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

@app.route('/add-to-cart', methods=['POST'])
def add_to_cart():
    if 'cart' not in session:
        session['cart'] = []

    form = AddToCart()

    if form.validate_on_submit():
        session['cart'].append({'menu_id' : form.menu_id.data, 'quantity' : form.quantity.data})
        session.modified = True

    return redirect(url_for('menu_page'))


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

        menu_items.append({'menu_id': menu_item.id, 'dish_name': menu_item.name, 'price': menu_item.price,
                         'quantity': quantity, 'total': total, 'index': index})
        index += 1

    grand_total_plus_tax = grand_total * 1.07

    return render_template('cart.html', menu_items=menu_items, grand_total=grand_total,
                           grand_total_plus_shipping=grand_total_plus_tax)

@app.route('/remove-from-cart/<index>')
def remove_from_cart(index):
    del session['cart'][int(index)]
    session.modified = True
    return redirect(url_for('cart'))

@app.route('/checkout')
def checkout():
    return render_template('checkout.html')

@app.route('/order', methods=['GET', 'POST'])
def order_page():
    menu = MenuItem.query.all()
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM menu")
    data = cursor.fetchall()
    return render_template('order.html', data=data, menu=menu)

"""
def array_merge(first_array, second_array):
    if isinstance(first_array, list) and isinstance(second_array, list):
        return first_array + second_array
    elif isinstance(first_array, dict) and isinstance(second_array, dict):
        return dict(list(first_array.items()) + list(second_array.items()))
    elif isinstance(first_array, set) and isinstance(second_array, set):
        return first_array.union(second_array)
    return False


@app.route('/add', methods=['POST'])
def add_product_to_cart():
    cursor = None

    _quantity = int(request.form['quantity'])
    _id = request.form['menu_id']

    if _quantity and _id and request.method == 'POST':
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM menu WHERE menu_id=%s", _id)
        row = cursor.fetchone()
        itemArray = {row['menu_id']: {'name': row['name'], 'menu_id': row['menu_id'], 'quantity': _quantity,
                                      'price': row['price'],
                                      'total_price': _quantity * row['price']}}

    all_total_price = 0
    all_total_quantity = 0

    session.modified = True
    if 'cart_item' in session:
        if row['menu_id'] in session['cart_item']:
            for key, value in session['cart_item'].items():
                if row['menu_id'] == key:
                    old_quantity = session['cart_item'][key]['quantity']
                    total_quantity = old_quantity + _quantity
                    session['cart_item'][key]['quantity'] = total_quantity
                    session['cart_item'][key]['total_price'] = total_quantity * row['price']
        else:
            session['cart_item'] = array_merge(session['cart_item'], itemArray)

        for key, value in session['cart_item'].items():
            individual_quantity = int(session['cart_item'][key]['quantity'])
            individual_price = float(session['cart_item'][key]['total_price'])
            all_total_quantity = all_total_quantity + individual_quantity
            all_total_price = all_total_price + individual_price
    else:
        session['cart_item'] = itemArray
        all_total_quantity = all_total_quantity + _quantity
        all_total_price = all_total_price + _quantity * row['price']

    session['all_total_quantity'] = all_total_quantity
    session['all_total_price'] = all_total_price

    return redirect(url_for('cart_page'))

    cursor.close()
    conn.close()


@app.route('/empty')
def empty_cart():
 try:
  session.clear()
  return redirect(url_for('.products'))
 except Exception as e:
  print(e)


@app.route('/cart')
def cart_page():
    return render_template('cart.html')
"""

if __name__ == '__main__':
    app.run(debug=True)
