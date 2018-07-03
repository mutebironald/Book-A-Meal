from flask_bcrypt import Bcrypt
import jwt
from datetime import datetime, timedelta
from flask import jsonify, make_response

from app.__init__ import db, secret
import datetime

from app import db


class User(db.Model):
    """Defines the 'User' model mapped to database table 'user'."""
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(145), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    admin = db.Column(db.Boolean, default=False)
    orders = db.relationship('Order', backref='user')

    def __init__(self, email, password):
        """Initialize the user with an email and a password."""
        self.email = email
        self.password = Bcrypt().generate_password_hash(password).decode('utf-8')

    def password_is_valid(self, password):
        """Checks the password against its hash to validate the user's password"""
        return Bcrypt().check_password_hash(self.password, password)

    def __repr__(self):
        """Returns a User model representation"""
        return "User (%d, %s, %s, %s)" % (
            self.id, self.email, self.admin, self.orders)

    def save(self):
        """Save a user to the database."""
        db.session.add(self)
        db.session.commit()

    def generate_token(self, user_id):
        """Generates the access token"""
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + timedelta(minutes=60),
                'sub': user_id
            }

            jwt_string = jwt.encode(
                payload,
                secret,
                algorithm='HS256'
            )

            return jwt_string

        except Exception as e:
            return str(e)

    @staticmethod
    def decode_token(token):
        """Decodes the access token from the Authorization header."""
        try:
            payload = jwt.decode(token, secret)
            return payload['sub']

        except jwt.ExpiredSignatureError:
            return "Expired token. Please login to get a new token."

        except jwt.InvalidTokenError:
            return "Invalid token. Please register or login."


class Meal(db.Model):
    """Defines the 'Meal' model mapped to database table 'meal'."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(46), nullable=False, unique=True)
    price = db.Column(db.Integer, nullable=False)
    menus = db.relationship('Menu', backref='meal')

    def __init__(self, name, price):
        """Initialises the meal model"""
        self.name = name
        self.price = price

    def save(self):
        """Saves item to the Meal table"""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Removes item from meal table"""
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_meals():
        """Retrieves all meals present in the meal table"""
        results = []
        meals = Meal.query.all()
        if meals:
            for meal in meals:
                obj = {
                    "id": meal.id,
                    "name": meal.name,
                    "price": meal.price,
                }
                results.append(obj)
            response = jsonify(results)
            response.status_code = 200
            return response
        else:
            return "No meals present", 400

    @staticmethod
    def get_meal(id):
        meal = Meal.query.filter_by(id=id).first()
        if not meal:
            return make_response("That meal is not present", 400)
        results = []
        obj = {
            'id': meal.id,
            'name': meal.name,
            'price': meal.price
        }
        results.append(obj)
        return make_response(jsonify(results), 200)

    @staticmethod
    def create_meal(name, price):
        meal = Meal(name, price)
        meal.save()
        response = jsonify({
            'id': meal.id,
            'name': meal.name,
            'price': meal.price,
        })
        response.status_code = 201
        return response

    @staticmethod
    def update_meal(id, name, price):
        meal = Meal.query.filter_by(id=id).first()
        if not meal:
            abort(404)

        meal.name = name
        meal.price = price
        meal.save()
        response = jsonify({
            'id': meal.id,
            'name': meal.name,
            'price': meal.price
        })

        response.status_code = 200
        return response

    @staticmethod
    def delete_meal(id):
        meal = Meal.query.filter_by(id=id).first()
        if meal:
            Meal.delete(meal)
            response = make_response(
                'The meal has been deleted', 200)
            return response
        return "The meal specified is not present", 400

    def __repr__(self):
        """Returns a representation of the meals"""
        return "Meal (%d, %s, %s )" % (
            self.id, self.name, self.price)


class Menu(db.Model):
    """Defines the 'Menu' model mapped to table 'menu'."""
    id = db.Column(db.Integer, primary_key=True)
    meal_id = db.Column(db.Integer, db.ForeignKey('meal.id'))
    day = db.Column(db.DateTime, default=datetime.datetime.today())
    orders = db.relationship('Order', backref='menu')

    def __init__(self, meal_id):
        """Initialises the menu model"""
        self.meal_id = meal_id

    def save(self):
        """Saves items to the menu table"""
        self.day = datetime.datetime.today()
        db.session.add(self)
        try:
            db.session.commit()
        except BaseException:
            db.session.rollback()

    @staticmethod
    def get_menu():
        """Retrieves all the menu items"""
        menus = Menu.query.all()
        if not menus:
            return make_response("No menu present", 400)
        results = []
        for menu in menus:
            obj = {
                'id': menu.id,
                'name': menu.meal.name,
                'price': menu.meal.price,
                'day': menu.day
            }
            results.append(obj)
        response = jsonify(results)
        response.status_code = 200
        return response

    @staticmethod
    def setup_menu(id):
        menu = Menu(meal_id=id)
        menu.save()
        return make_response(
            {"MENU": {
                'id': menu.id,
                'name': menu.meal.name,
                'price': menu.meal.price,
                'day': datetime.datetime.utcnow()
            }
            }), 201

    def __repr__(self):
        return "Menu (%d,%s, %s, %s, %s )" % (
            self.id, self.name, self.meal_id, self.day)


class Order(db.Model):
    """Defines the 'Order' mapped to database table 'order'."""
    id = db.Column(db.Integer, primary_key=True)
    menu_id = db.Column(db.Integer, db.ForeignKey('menu.id'))
    order_time = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, user_id, menu_id):
        """Initialises the order tables"""
        self.user_id = user_id
        self.menu_id = menu_id

    def add_order(self):
        """Saves items to the order table"""
        self.order_time = datetime.datetime.now()
        db.session.add(self)
        return Order.save()

    def delete(self, x):
        """Removes items from the order table"""
        db.session.delete(x)
        Order.save()

    @staticmethod
    def save():
        try:
            db.session.commit()
            return True
        except BaseException:
            db.session.rollback()
            return False

    @staticmethod
    def get_all_orders():
        """Retrieves all orders present"""
        orders = []
        raw_orders = Order.query.all()
        for order in raw_orders:
            orders.append(order.to_dictionary())
        return orders

    def to_dictionary(self):
        """Return a dictionary representation of the order"""
        return dict(
            order_id=self.id,
            user_id=self.user_id,
            meal=self.menu.meal.name,
            price=self.menu.meal.price,
            order_time=self.order_time)

    def __repr__(self):
        """Returns a string representation of the order table"""
        return "Order(%d, %s, %s, %s, %s )" % (
            self.id, self.menu_name, self.admin_id, self.order_time, self.user_id)
