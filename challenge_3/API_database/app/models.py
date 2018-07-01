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
        # return Meal.query.all()
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
        return "Meal (%d, %s, %s )" %(
            self.id, self.name, self.price)

class Menu(db.Model):
    """Defines the 'Menu' model mapped to table 'menu'."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False, unique=True)
    meal_id = db.Column(db.Integer, db.ForeignKey('meal.id'))
    day = db.Column(db.String(50), default=datetime.datetime.today())
    orders = db.relationship('Order', backref='menu')

    def __init__(self, name, day):
        """Initialises the menu model"""
        self.name = name
        self.day = day

    def save(self):
        """Saves items to the menu table"""
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_menu():
        """Retrieves all the menu items"""
        menus = Menu.query.all()
        if not menus:
            return make_response("No menu present", 400)
        results = []
        print("hshs----")
        # print(menus)
        for menu in menus:
            print("check this")
            print(menu.day)
            print(menu)
            print(menu.price)
            print("now done")
            obj={
                'id': menu.id,
                'name': menu.name,
                'day': menu.day
                }
            results.append(obj)
        response = jsonify(results)
        response.status_code = 200
        return response

    @staticmethod
    def setup_menu(id):
        meal = Meal.query.filter_by(id=id).first()
        # meal = Menu.query.filter_by(meal_id=id).first()
        if meal:
            menu = Menu(meal.name, meal.price)
            menu.save()
            return make_response(
                {"MENU": {
                'id': menu.id,
                'name': menu.name,
                'price': meal.price,
                'day': datetime.datetime.utcnow()
            }
            }), 201

        # menu = Menu(name=name, day=day)
        # menu.save()
        # print("meee")
        # print(menu)
        # response=jsonify({
        #     'id': menu.id,
        #     'name': menu.name,
        #     'day': menu.day
        #     })
        # response.status_code=201
        # return response

    def __repr__(self):
        return "Menu (%d,%s, %s, %s, %s )" %(
            self.id, self.name, self.admin_id, self.meal_id, self.day)

class Order(db.Model):
    """Defines the 'Order' mapped to database table 'order'."""
    id = db.Column(db.Integer, primary_key=True)
    menu_id = db.Column(db.Integer, db.ForeignKey('menu.id'))
    order_time = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) 

    def __init__(self, order_time):
        """Initialises the order tables"""
        self.order_time = order_time

    def save(self):
        """Saves items to the order table"""
        db.session.add(self)
        db.session.commit()

    def delete(self, x):
        """Removes items from the order table"""
        db.session.delete(x)
        db.session.commit()

    @staticmethod
    def get_all_orders():
        """Retrieves all orders present"""
        return Order.query.all()

    def __repr__(self):
        """Returns a string representation of the order table"""
        return "Order(%d, %s, %s, %s, %s )" %(
            self.id, self.menu_name, self.admin_id, self.order_time, self.user_id)
