# from flask_sqlalchemy import SQLAlchemy

# # from app import db
from flask_bcrypt import Bcrypt
import jwt
from datetime import datetime, timedelta

# db = SQLAlchemy()
from app import db, secret
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
        return "User (%d, %s, %s, %s)" %(
            self.id, self.email, self.admin, self.orders)

    def save(self):
        """Save a user to the database."""
        db.session.add(self)
        db.session.commit()

    def generate_token(self, user_id):
        """Generates the access token"""
        try:
            payload = {
                'exp':datetime.datetime.utcnow()  + timedelta(minutes=60),
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
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(46), nullable=False, unique=True)
    price = db.Column(db.Integer, nullable=False)
    menus = db.relationship('Menu', backref='meal')

    def __init__(self, name, price):
        self.name = name
        self.price = price

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_meals():
        return Meal.query.all()

    def __repr__(self):
        return "Meal (%d, %s, %s )" %(
            self.id, self.name, self.price)

class Menu(db.Model):
    """Defines the 'Menu' model mapped to table 'menu'."""
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(40), nullable=False, unique=True)
    meal_id = db.Column(db.Integer, db.ForeignKey('meal.id'))
    day = db.Column(db.String(50), default=datetime.datetime.today())
    orders = db.relationship('Order', backref='menu')

    def __init__(self, name, day):
        self.name = name
        self.day = day

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all_menu():
        return Menu.query.all()

    def __repr__(self):
        return "Menu (%d,%s, %s, %s, %s )" %(
            self.id, self.name, self.admin_id, self.meal_id, self.day)

class Order(db.Model):
    """Defines the 'Order' mapped to database table 'order'."""
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    menu_id = db.Column(db.Integer, db.ForeignKey('menu.id'))
    order_time = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) 

    def __init__(self, order_time):
        self.order_time = order_time

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self, x):
        db.session.delete(x)
        db.session.commit()

    @staticmethod
    def get_all_orders():
        return Order.query.all()

    def __repr__(self):
        return "Order(%d, %s, %s, %s, %s )" %(
            self.id, self.menu_name, self.admin_id, self.order_time, self.user_id)