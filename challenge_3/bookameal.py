from apispec import APISpec
from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify, make_response, request, json, abort
import os, binascii

from flask_bcrypt import Bcrypt
import datetime

import jwt

from flasgger import Swagger


#creating an APISpec
# spec = APISpec(
#     title='Book-A-Meal API',
#     version='1.0.0',
#     info=dict(
#         description='A meal booking API'
#         ),
#     plugins=[
#         'apispec.ext.flask'
#         ],
#     )

app = FlaskAPI(__name__)
app.config.from_object('config.ConfigDevelopment')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres@localhost:5432/test_bookameal'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = binascii.hexlify(os.urandom(24))

#db.init_app(app)
db = SQLAlchemy(app)
Swagger(app)

#models start here

class User(db.Model):
    """Defines the 'User' model mapped to database table 'user'."""
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(145), nullable=False, unique=True)
    password = db.Column(db.String(170), nullable=False)
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
                'exp':datetime.datetime.utcnow()  + datetime.timedelta(minutes=60),
                'sub': user_id
                }
            
            jwt_string = jwt.encode(
                payload,
                app.config['SECRET_KEY'],
                algorithm='HS256'
                )
            return jwt_string
            

        except Exception as e:
            return str(e)
        
    @staticmethod
    def decode_token(token):
        """Decodes the access token from the Authorization header."""
        try:
            payload = jwt.decode(token, app.config['SECRET_KEY'])
            return payload['sub']

        except jwt.ExpiredSignatureError:
            return "Expired token. Please login to get a new token."

        except jwt.InvalidTokenError:
            return "Invalid token. Please register or login."
                
"""
class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(145), unique=True)
    #user_id is it correct
    user_id = db.Column(db.Integer)
    admin = db.Column(db.Boolean, default=True)
    meals = db.relationship('Meal', backref='admin')
    #menu = db.relationship('Menu', backref='admin')

    def save(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return "Admin(%d, %s, %s, %s, %s, %s)" %(
            self.id, self.email, self.user_id, self.admin, self.meals, self.menu)
"""

class Meal(db.Model):
    """Defines the 'Meal' model mapped to database table 'meal'."""
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(46), nullable=False, unique=True)
    price = db.Column(db.Integer, nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))
    menus = db.relationship('Menu', backref='meal')

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
        return "Meal(%d, %s, %s, %s )" %(
            self.id, self.name, self.price)

class Menu(db.Model):
    """Defines the 'Menu' model mapped to table 'menu'."""
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(40), nullable=False, unique=True)
    #admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))
    meal_id = db.Column(db.Integer, db.ForeignKey('meal.id'))
    day = db.Column(db.String(50), default=datetime.datetime.today())
    orders = db.relationship('Order', backref='menu')

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
    #menu_name = db.Column(db.String(40), db.ForeignKey('menu.name'))
    menu_id = db.Column(db.Integer, db.ForeignKey('menu.id'))
    #admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))
    order_time = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) 

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
#end of the models

@app.route('/')
def home():
    """
    Home route
    ---
    tags:
      - Book-A-Meal API
    parameters:
      - name: language
        in: path
        type: string
        required: true
        description: The language name
      - name: size
        in: query
        type: integer
        description: size of awesomeness
    responses:
            200:
                description: Receives welcome message.
    """
    
    """Starting point of the API"""
    return "Welcome to Book-A-Meal."

#user routes
@app.route('/api/v1/auth/signup', methods=['POST'])
def register():
    """
    Registration route
    ---
    tags:
      - Book-A-Meal API
    parameters:
      - name: language
        in: path
        type: string
        required: true
        description: The language name
      - name: size
        in: query
        type: integer
        description: size of awesomeness
    responses:
        201:
            description: Successfull registration of user
        401:
            description: Unsuccessful user registration
        202:
            description: Double signup rejection
    """

        
    user = User.query.filter_by(email=request.data['email']).first()

    if not user:
        try:
            data = request.data

            email = data['email']
            password = data['password']
            user = User(email=email, password=password)
            user.save()

            response ={
                'message': 'You are now registered'
                }
            return make_response(jsonify(response)), 201
        except Exception as e:
            
            response = {
                "message" : str(e)
                }
            return make_response(jsonify(response)), 401
        
    else:
        return make_response("The user already exists", 202)
        

@app.route('/api/v1/auth/login', methods=['POST'])
def login():
    """
    Login route
    ---
    tags:
      - Book-A-Meal API
    parameters:
      - name: language
        in: path
        type: string
        required: true
        description: The language name
      - name: size
        in: query
        type: integer
        description: size of awesomeness
    responses:
        200:
            description: A successfully logged in user receives an access_token
        401:
            description: A user with wrong log in credentials is informed
    """
    user = User.query.filter_by(email=request.data['email']).first()  

    if user and user.password_is_valid(request.data['password']):
        access_token = user.generate_token(user.id)
        if access_token:
            response = {
                'message': 'You logged in successfully.',
                'access_token': access_token.decode()
                }
            return make_response(jsonify(response)), 200
            
    else:
        response = {
            'message': 'Invalid email or password'
                }
        return make_response(jsonify(response)), 401



#meals routes
@app.route('/api/v1/meals')
def account_get_meals():
    """
    Meals route
    ---
    tags:
      - Book-A-Meal API
    parameters:
      - name: language
        in: path
        type: string
        required: true
        description: The language name
      - name: size
        in: query
        type: integer
        description: size of awesomeness
    responses:
        400:
            description: No meals present
        200:
            description: Meals are present
    """
    auth_header = request.headers.get('Authorization')
    
    access_token = auth_header
    if access_token:
        user_id = User.decode_token(access_token)
        if not isinstance(user_id, str):

    
            meals = Meal.get_meals()
            if not meals:
                return make_response("No meals present", 400)
            results = []

            for meal in meals:
                obj = {
                    'id': meal.id,
                    'name': meal.name,
                    'price': meal.price,
                    #'admin_id': meal.admin_id
                    }
                results.append(obj)
            response = jsonify(results)
            response.status_code = 200
            return response
        else:
            return jsonify(user_id)

@app.route('/api/v1/meals/<int:id>', methods=['GET'])
def account_get_specific_meal(id):
    """
    Meals route
    ---
    tags:
      - Book-A-Meal API
    parameters:
      - name: language
        in: path
        type: string
        required: true
        description: The language name
      - name: size
        in: query
        type: integer
        description: size of awesomeness
    responses:
        400:
            description: The meal with the specified id is absent
        200:
            description: The meal is successfully returned.
    """
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

@app.route('/api/v1/meals', methods=['POST'])
def account_create_meal():
    """
    Meals route
    ---
    tags:
      - Book-A-Meal API
    parameters:
      - name: language
        in: path
        type: string
        required: true
        description: The language name
      - name: size
        in: query
        type: integer
        description: size of awesomeness
    responses:
        201:
            description: The meal has been created.
    """
    access_token = request.headers.get('Authorization')
    if access_token:
        user_id = User.decode_token(access_token)
        print(user_id)
        if not isinstance(user_id, str):
            name = str(request.data.get('name', ''))
            price = int(request.data.get('price', ''))
            if name and price:
                meal = Meal(name=name, price=price)
                meal.save()
                response = jsonify({
                    'id': meal.id,
                    'name': meal.name,
                    'price': meal.price,
                    #'admin_id': meal.admin_id
                    })
                response.status_code = 201
                return response
        else:
            return jsonify(user_id)

@app.route('/api/v1/meals/<int:id>', methods=['PUT'])
def account_update_meal(id):
    """
    Meals route
    ---
    tags:
      - Book-A-Meal API
    parameters:
      - name: language
        in: path
        type: string
        required: true
        description: The language name
      - name: size
        in: query
        type: integer
        description: size of awesomeness
    responses:
        404:
            description: The meal you want to update is not in the database.
        200:
            description: The meal has been successfully updated.
    """
    access_token = request.headers.get('Authorization')
    if access_token:
        user_id = User.decode_token(access_token)
        if not isinstance(user_id, str):
    
            meal = Meal.query.filter_by(id=id).first()
            if not meal:
                abort(404)
        
            name = str(request.data.get('name', ''))
            price = int(request.data.get('price', ''))
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
        else:
            return jsonify(user_id)
        
    


@app.route('/api/v1/meals/<int:id>', methods=['DELETE'])
def account_delete_meal(id):
    """Meals route.
    get:
        summary: meals endpoint.
        description: Delete a specific meal
        parameters:
            - name: id
              in: path
              type: integer
              required: true
    responses:
        200:
            description: The meal with the ID specified has been deleted
    """
    access_token=request.headers.get('Authorization')
    if access_token:
        user_id=User.decode_token(access_token)
        if not isinstance(user_id, str):
            
            meal = Meal.query.filter_by(id=id).first()
            Meal.delete(meal)
            response = make_response(
                'The meal has been deleted', 200)
            return response
        else:
            return jsonify(user_id)
    
    

#menu routes
@app.route('/api/v1/menu')
def get_menu():
    """
    Menu route
    ---
    tags:
      - Book-A-Meal API
    parameters:
      - name: language
        in: path
        type: string
        required: true
        description: The language name
      - name: size
        in: query
        type: integer
        description: size of awesomeness
    respnses:
        400:
            description: There is no menu present.
        200:
            description: The menu has successfully been returned.
    """
    access_token = request.headers.get('Authorization')
    if access_token:
        user_id = User.decode_token(access_token)
        
        if not isinstance(user_id, str):

            menus = Menu.get_all_menu()
            if not menus:
                return make_response("No menu present", 400)
            results = []
            for menu in menus:
                obj={
                    'id': menu.id,
                    'name': menu.name,
                    'day': menu.day
                    }
                results.append(obj)
            response = jsonify(results)
            response.status_code = 200
            return response
        else:
            return jsonify(user_id)

@app.route('/api/v1/menu', methods=['POST'])
def setup_menu():
    """
    Menu route
    ---
    tags:
      - Book-A-Meal API
    parameters:
      - name: language
        in: path
        type: string
        required: true
        description: The language name
      - name: size
        in: query
        type: integer
        description: size of awesomeness
    responses:
        201:
            description: The menu has been successfully returned.
    """
    access_token = request.headers.get('Authorization')

    if access_token:
        user_id = User.decode_token(access_token)
        if not isinstance(user_id, str):
            name = str(request.data.get('name', ''))
            day = str(request.data.get('day', ''))
            if name and day:
                menu = Menu(name=name, day=day)
                menu.save()
                response=jsonify({
                    'id': menu.id,
                    'name': menu.name,
                    'day': menu.day
                    })
                response.status_code=201
                return response
        else:
            return jsonify(user_id)


#orders routes
#@app.route('/api/v1/orders')
#def add_order():
    #pass
    

@app.route('/api/v1/orders')
def get_all_orders():
    """
    Orders route
    ---
    tags:
      - Book-A-Meal API
    parameters:
      - name: language
        in: path
        type: string
        required: true
        description: The language name
      - name: size
        in: query
        type: integer
        description: size of awesomeness
    responses:
        200:
            description: Successfully returned all the orders present.
        400:
            description: No orders present at the moment.
    """
    access_token=request.headers.get('Authorization')
    if access_token:
        user_id = User.decode_token(access_token)
        if not isinstance(user_id, str):
            orders = Order.get_all_orders()
            if orders:
                results = []
                for order in orders:
                    obj = {
                        'id': order.id,
                        'order_time': order.order_time
                        }
                    results.append(obj)
                response = jsonify(results)
                response.status_code=200
                return response
            else:
                return make_response("No orders present", 400)
        else:
            return jsonify(user_id)
    

@app.route('/api/v1/orders/<int:id>', methods=["DELETE"])
def remove_order(id):
    """
    Orders route
    ---
    tags:
      - Book-A-Meal API
    delete:
        summary: Order endpoint.
        description: Delete an order with the specified ID from the database.
    parameters:
        - name: id
        in: path
        description: Order ID
        type: integer
        required: true
    responses:
        200:
            description: The order has been deleted.
        400:
            description: The order specified is not present.

    """
                
    access_token = request.headers.get('Authorization')
    if access_token:
        user_id = User.decode_token(access_token)
        if not isinstance(user_id, str):
            order = Order.query.filter_by(id=id).first()
            if not order:
                return make_response("The order specified is not present"), 400
            #Meal.delete(order)
            Order.delete(order)
            response = make_response(
                "The order has been deleted", 200)
            return response
        else:
            return jsonify(user_id)    

if __name__ == "__main__":
    # app.run(debug=True)
    app.run(debug=True)

