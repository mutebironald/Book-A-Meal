from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from flask import request, jsonify, abort, make_response

import os, binascii

from instance.config import app_config

db = SQLAlchemy()
secret = binascii.hexlify(os.urandom(24))

def create_app(config_name):
    # from app.models import User, Meal, Menu, Order
    from app.models import User, Meal, Menu, Order

    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = secret
    with app.app_context():
        db.init_app(app)

    
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
                Order.session.delete(order)
                response = make_response(
                    "The order has been deleted", 200)
                return response
            else:
                return jsonify(user_id)   

    from .auth import auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app