# THIS IS IMPORTING THE DIFFERENT MODULES
import hmac
import sqlite3
import datetime
from flask_mail import Mail, Message
from flask import Flask, request, jsonify
from flask_jwt import JWT, jwt_required
from flask_cors import CORS


# THIS IS TO CREATE AND INITIALIZE THE USER CLASSES
class User(object):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password


# THIS THE CREATION OF THE PRODUCT PAGE
class Product(object):
    def __init__(self, product_id, product, category, description, dimensions, price):
        self.product_id = product_id
        self.product = product
        self.category = category
        self.description = description
        self.dimensions = dimensions
        self.price = price


# THIS IS WILL FETCH ALL THE USERS
def fetch_users():
    with sqlite3.connect('pos.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user")
        users = cursor.fetchall()

        new_data = []

        for data in users:
            new_data.append(User(data[0], data[4], data[5]))
    return new_data


# THIS IS CREATING AND INITIALIZING A DATABASE CLASS
class Database():
    def __init__(self):
        self.conn = sqlite3.connect('pos.db')
        self.cursor = self.conn.cursor()

    def registration(self, value):
        self.cursor.execute("INSERT INTO user(name, surname, email, username, password) VALUES (?, ?, ?, ?, ?)", value)
        self.conn.commit()

    def edit_profile(self, incoming_data, id):
        response = {}
        put_data = {}

        if incoming_data.get('name') is not None:
            put_data['name'] = incoming_data.get('name')
            with sqlite3.connect('pos.db') as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE user SET name =? WHERE id =?", (put_data['name'], id))
                conn.commit()
                response['status_code'] = 200
                response['message'] = "Name successfully updated"

        if incoming_data.get('surname') is not None:
            put_data['surname'] = incoming_data.get('surname')
            with sqlite3.connect('pos.db') as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE user SET surname =? WHERE id=?", (put_data['surname'], id))
                conn.commit()
                response['status_code'] = 200
                response['message'] = "Surname successfully updated"

        if incoming_data.get('email') is not None:
            put_data['email'] = incoming_data.get('email')
            with sqlite3.connect('pos.db') as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE user SET email =? WHERE id=?", (put_data['email'], id))
                conn.commit()
                response['status_code'] = 200
                response['message'] = "ID number successfully updated"

        if incoming_data.get('username') is not None:
            put_data['username'] = incoming_data.get('username')
            with sqlite3.connect('pos.db') as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE user SET username =? WHERE id=?", (put_data['username'], id))
                conn.commit()
                response['status_code'] = 200
                response['message'] = "Username successfully updated"

        if incoming_data.get('password') is not None:
            put_data['password'] = incoming_data.get('password')
            with sqlite3.connect('pos.db') as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE user SET password =? WHERE id=?", (put_data['password'], id))
                conn.commit()
                response['status_code'] = 200
                response['message'] = "Password successfully updated"

    def delete_profile(self, value):
        query = ("DELETE FROM user WHERE id=".format(value))
        self.cursor.execute(query)
        self.conn.commit()

    def add_product(self, value):
        query = ("INSERT INTO product (product, category, description, dimensions, price, id) "
                           "VALUES(?, ?, ?, ?, ?, ?)".format(value))
        self.cursor.execute(query)
        self.conn.commit()

    def edit_product(self, incoming_data, product_id):
        response = {}
        put_data = {}

        if incoming_data.get('product') is not None:
            put_data['product'] = incoming_data.get('product')
            with sqlite3.connect('pos.db') as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE product SET product =? WHERE product_id=?", (put_data['product'], product_id))
                conn.commit()
                response['status_code'] = 200
                response['message'] = "Product successfully updated."

        if incoming_data.get('category') is not None:
            put_data['category'] = incoming_data.get('category')
            with sqlite3.connect('pos.db') as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE product SET category =? WHERE product_id=?", (put_data['category'], product_id))
                conn.commit()
                response['status_code'] = 200
                response['message'] = "Category successfully updated."

        if incoming_data.get('description') is not None:
            put_data['description'] = incoming_data.get('description')

            with sqlite3.connect('pos.db') as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE product SET description =? WHERE product_id=?",
                               (put_data['description'], product_id))
                conn.commit()
                response['status_code'] = 200
                response['message'] = "Description was successfully updated."

        if incoming_data.get('dimensions') is not None:
            put_data['dimensions'] = incoming_data.get('dimensions')

            with sqlite3.connect('pos.db') as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE product SET dimensions=? WHERE product_id=?",
                               (put_data['dimensions'], product_id))
                conn.commit()
                response['status_code'] = 200
                response['message'] = "Dimensions was successfully updated."

        if incoming_data.get('price') is not None:
            put_data['price'] = incoming_data.get('price')

            with sqlite3.connect('pos.db') as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE product SET price=? WHERE product_id=?",
                               (put_data['price'], product_id))
                conn.commit()
                response['status_code'] = 200
                response['message'] = "Price was successfully updated."

        if incoming_data.get('id') is not None:
            put_data['id'] = incoming_data.get('id')

            with sqlite3.connect('pos.db') as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE product SET id=? WHERE product_id=?",
                               (put_data['id'], product_id))
                conn.commit()
                response['status_code'] = 200
                response['message'] = "ID was successfully updated."

    def delete_product(self, value):
        query = ("DELETE FROM product WHERE product_id='{}'".format(value))
        self.cursor.execute(query)
        self.conn.commit()

    def show_products(self):
        query = ("SELECT * FROM product")
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def view_product(self, value):
        response = {}
        query = ("SELECT * FROM product WHERE product_id='{}'".format(value))
        self.cursor.execute(query)
        response['data'] = self.cursor.fetchone()

    def view_users_products(self, value):
        response = {}
        query = ("SELECT * FROM product WHERE id='{}'".format(value))



# THIS IS FECTHING ALL THE PRODUCTS
def fetch_products():
    with sqlite3.connect('pos.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM product")
        products = cursor.fetchall()

        new_product = []

        for data in products:
            new_product.append(Product(data[0], data[1], data[2], data[3], data[4], data[5]))
    return new_product

# Creating a product table
def init_product_table():
    with sqlite3.connect('pos.db') as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS product (product_id INTEGER PRIMARY KEY AUTOINCREMENT,"
                     "product TEXT NOT NULL, category TEXT NOT NULL, description TEXT NOT NULL, "
                     "dimensions TEXT NOT NULL, price TEXT NOT NULL)")
        print("successfully created product table.")

init_product_table()
user = fetch_products()
products = fetch_products()


# THIS WILL CREATE A THE USER TABLE
def init_user_table():
    conn = sqlite3.connect('pos.db')
    print('Database succesfully opened.')

    conn.execute("CREATE TABLE IF NOT EXISTS user (id INTEGER PRIMARY KEY AUTOINCREMENT,"
                 "name TEXT NOT NULL, surname TEXT NOT NULL, email TEXT NOT NULL, username TEXT NOT NULL,"
                 "password TEXT NOT NULL)")
    print("User table has been succefully created")
    conn.close()


def init_cart_table():
    with sqlite3.connect('pos.db') as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS cart (product_id INTEGER FOREIGN KEY)")


init_user_table()
init_product_table()
users = fetch_users()

username_table = {u.username: u for u in users}
userid_table = {u.id: u for u in users}


def authenticate(username, password):
    user = username_table.get(username, None)
    if user and hmac.compare_digest(user.password.encode('utf-8'), password.encode('utf-8')):
        return user


def identity(payload):
    id = payload['identity']
    return userid_table.get(id, None)


#   THIS IS THE INITIALIZING OF THE APP
app = Flask(__name__)
CORS(app)
app.debug = True
app.config['SECRET_KEY'] = 'super-secret'
app.config['JWT_EXPIRATION_DELTA'] = datetime.timedelta(hours=20)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'ifyshop965@gmail.com'
app.config['MAIL_PASSWORD'] = 't3amShopify'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

jwt = JWT(app, authenticate, identity)


# THIS IS THE USER REGISTRATION ROUTE AND THE FUNCTION
@app.route('/registration/', methods=["POST"])
def registration():
    db = Database
    response = {}

    if request.method == "POST":

        name = request.form['name']
        surname = request.form['surname']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        with sqlite3.connect('pos.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM user WHERE username='{}'".format(username))
            registered_username = cursor.fetchone()

        if name == '' or surname == '' or email == '' or username == '' or password == '':
            response['status_code'] = 400
            response['message'] = "Error! Please enter all fields."
            return response

        if registered_username:
            response['username'] = username
            response['status_code'] = 400
            response['message'] = "Username already taken. Please enter a unique username."
            return response

        values = (name, surname, email, username, password)
        db.registration(Database(), values)
        response["message"] = "New user successfully registered"
        response["status_code"] = 200

        mail = Mail(app)
        msg = Message("Welcome!", sender='ifyshop965@gmail.com', recipients=[email])
        msg.body = "Good morning/afternoon {}.\n".format(name)
        msg.body = msg.body + "Your have successfully registered your profile on our site with the username {}.\n"\
            .format(username)
        msg.body = msg.body + "Please feel free to send us email if you have any queries or concerns.\n \n" \
                              "Kind regards,\n Shopify Team"
        mail.send(msg)

        return response


# THIS IS THE USER LOGIN AND THE FUNCTION
@app.route('/login/', methods=["POST"])
def login():
    response = {}

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        with sqlite3.connect('pos.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM user WHERE username=? AND password=?", (username, password))
            registered_user = cursor.fetchone()

        if username == '':
            response['status_code'] = 400
            response['message'] = "Error! Please enter your username."
            return response

        if password == '':
            response['status_code'] = 400
            response['message'] = "Error! Please enter your password."
            return response

        if registered_user:
            response['registered_user'] = registered_user
            response['status_code'] = 200
            response['message'] = "Successfully logged in"
            return response

        else:
            response['status_code'] = 400
            response['message'] = "Login unsuccessful. Please try again."
        return jsonify(response)


# THIS IS THE DISPLAY ALL USER ROUTE AND FUNCTION
@app.route('/git ', methods=["GET"])
def display_users():
    response = {}
    with sqlite3.connect("pos.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user")

        all_users = cursor.fetchall()

    response['status_code'] = 200
    response['data'] = all_users
    return response


# THIS IS THE VIEW SPECIFIC USER PROFILE ROUTE AND FUNCTION
@app.route('/view-profile/<int:id>/', methods=["GET"])
@jwt_required()
def view_profile(id):
    response = {}

    with sqlite3.connect('pos.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user WHERE id=?", (str(id)))

        response['status_code'] = 200
        response['message'] = "Profile retrieved successfully"
        response['data'] = cursor.fetchone()

    return jsonify(response)


# Edit users profile route and function
@app.route('/edit-profile/<int:id>/', methods=["PUT"])
@jwt_required()
def edit_profile(id):
    response = {}

    if request.method == "PUT":
        incoming_data = dict(request.json)
        db = Database()
        db.edit_profile(incoming_data, id)

    return response


# Delete a users profile route and function
@app.route('/delete-profile/<int:id>')
def delete_profile(id):
    response = {}
    db = Database()
    db.delete_profile(id)
    response['status_code'] = 200
    response['message'] = "Profile successfully deleted"
    return response


# THIS IS THE ADDING A NEW PRODUCT ROUTE AND FUNCTION
@app.route('/add-product/', methods=["POST"])
@jwt_required()
def add_product():
    db = Database()
    response = {}

    if request.method == "POST":
        product = request.form['product']
        category = request.form['category']
        description = request.form['description']
        dimensions = request.form['dimensions']
        price = request.form['price']
        id = request.form['id']

        values = (product, category, description, dimensions, price, id)
        db.add_product(values)
        response["status_code"] = 201
        response['description'] = "Product added successfully"
        return response


# THIS IS THE DELETING A SPECIFIC PRODUCT ROUTE AND FUNCTION
@app.route('/delete-product/<int:product_id>')
@jwt_required()
def delete_product(product_id):
    db = Database()
    response = {}
    db.delete_product(product_id)
    response['status_code'] = 200
    response['message'] = "Product successfully deleted"
    return response


# THIS IS THE EDITING A SPECIFIC PRODUCT ROUTE AND FUNCTION
@app.route('/edit-product/<int:product_id>/', methods=["PUT"])
@jwt_required()
def edit_product(product_id):
    response = {}

    if request.method == "PUT":
        incoming_data = dict(request.json)
        db = Database()
        db.edit_product(incoming_data, product_id)

    return response


# THIS IS TO DISPLAY ALL PRODUCTS ROUTE AND FUNCTION
@app.route('/show-products/', methods=["GET"])
@jwt_required()
def show_products():
    db = Database()
    response = {}

    products = db.show_products()
    response['status_code'] = 200
    response['data'] = products
    return response


# THIS WILL VIEW A SPECIFIC PRODUCT ROUTE AND FUNCTION
@app.route('/view-product/<int:product_id>', methods=["GET"])
@jwt_required()
def view_product(product_id):
    db = Database()
    response = {}

    db.view_product(product_id)
    response['status_code'] = 200
    response['description'] = "Product was successfully retrieved"

    return jsonify(response)


# THIS VIEWS A SPECIFIC USER PRODUCTS ROUTE AND FUNCTION
@app.route('/view-user-products/<int:id>/', methods=["GET"])
def view_user_products(id):
    response = {}

    with sqlite3.connect('pos.db') as conn:
        cursor = conn.cursor()
        cursor.execute()
        all_products = cursor.fetchall()

        response['status_code'] = 200
        response['message'] = "All products from user retrieved successfully"
        response['data'] = all_products

        return response


if __name__ == '__main__':
    app.debug = True
    app.run()
