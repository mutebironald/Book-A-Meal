from flask import  request, jsonify, make_response, json
from flask_login import  login_user, logout_user, current_user
from .classes.mockdbhelper import MOCK_USERS, MOCK_MEALS, MOCK_ORDERS, new_menu
from .classes.user import User
from . import app, PH, DB, basic_auth
from . import login_manager
import datetime
import re
from flasgger import Swagger

Swagger(app)

@login_manager.user_loader
def load_user(user_id):
    user_password = DB.get_user(user_id)
    if user_password:
        return User(user_id)


# from flask_login import current_user
# from flask import url_for, redirect
# from functools import wraps
# def requires_roles(*roles):
#     def wrapper(f):
#         @wraps(f)
#         def wrapped(*args, **kwargs):
#             if current_user.get_role() not in roles:
#                 return make_response('unauthorized', 401)
#             return f(*args, **kwargs)
#         return wrapped
#     return wrapper
# @requires_roles('admin')


@app.route('/')
def home():
    """
    This is the language awesomeness API
    Call this api passing a language name and get back its features
    ---
    tags:
      - Awesomeness Language API
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
      500:
        description: Error The language is not awesome!
      200:
        description: A language with its awesomeness
        schema:
          id: awesome
          properties:
            language:
              type: string
              description: The language name
              default: Lua
            features:
              type: array
              description: The awesomeness list
              items:
                type: string
              default: ["perfect", "simple", "lovely"]

    """
    #if not current_user.is_admin():
        #return 'sorry'
    #else:
    return "Welcome to Book-A-Meal"

@app.route('/api/v1/auth/signup', methods=["POST"])
def register():
    """Facilitates user registration"""
    data = request.get_json()
    email = data['email']
    if not re.match(r"([\w\.-]+)@([\w\.-]+)(\.[\w\.]+$)", email):
        return jsonify({"error": "Invalid email."})
    password = data['password']
    if password.strip() == "":
        return make_response("you must enter a password", 400)
    if len(password) < 5:
        return jsonify({"message": "Password too short"})
    if DB.get_user(email):
        return make_response("The email already exists", 409)
    salt = PH.get_salt()
    hashed = PH.get_hash(str(password) + str(salt))
    DB.add_user(email, salt, hashed)
    return make_response("You are now registered", 201)
    
@app.route('/api/v1/auth/login', methods=['POST'])
def login():
    """Facilitates user registration."""
    data = request.get_json()
    email = data['email']
    if email:
        password = data['password']
        if password:
            stored_user = DB.get_user(email)
            if stored_user and PH.validate_password(password, stored_user['salt'], stored_user['hashed']):
                user = User(email)
                login_user(user)
                return make_response("success!!, you are now logged in", 200)
            return make_response("Your email does not exist", 401)
        return make_response("You must enter a password", 400)
    return make_response("Your email field is empty", 400)

@app.route('/api/v1/meals')
@basic_auth.required
def account_get_meals():
    """Enables meal retrieval for authenticated user""" 
    meals = DB.get_meals(current_user.get_id())
    return make_response(jsonify({'MOCK_MEALS': meals}), 200)


@app.route('/api/v1/meals', methods=['POST'])
@basic_auth.required
def account_create_meal():
    """Enables Authenticated user to create meals"""
    data = request.get_json()
    meal_name = data['meal_name']
    price = data['price']
    if meal_name:
        meal_id = DB.add_meal(meal_name, price, current_user.get_id())
        DB.update_meal(meal_id, meal_name, price)
        return make_response("You successfully created a meal", 200)
 
    else:
        return make_response('Please enter a meal name', 400)

@app.route('/api/v1/meals/<meal_id>', methods=["PUT"])
@basic_auth.required
def account_update_meal(meal_id):
    """Authenticated user is able to update meal"""
    data = request.get_json()
    meal_name = data['meal_name']
    price = data['price']
    if meal_name:
        DB.update_meal(meal_id, meal_name, price)
        return jsonify({'meals': MOCK_MEALS}), 200

    else:
        return make_response('Please enter a meal name', 400)

@app.route('/api/v1/meals/<meal_id>', methods=["DELETE"])
@basic_auth.required
def account_delete_meal(meal_id):
    """Authenticated user is able to delete particular meal"""
    DB.delete_meal(meal_id)
    return make_response("The meal has been deleted", 202)
    #else:
        #return make_response("The meal is not present")

@app.route('/api/v1/orders', methods=['POST'])
@basic_auth.required
def new_order():
    """Enables customer to make an order"""
    data = request.get_json()
    meal_id = data["meal_id"]
    DB.add_order(meal_id, datetime.datetime.utcnow())
    return "Your order has been logged and a you will be served shortly"

@app.route('/api/v1/orders')
@basic_auth.required
def get_all_orders():
    """Enables Authenticated caterer is able to get all orders""" 
    now = datetime.datetime.utcnow()
    orders = DB.get_orders(current_user.get_id())
    for order in orders:
        deltaseconds = (now - order['time']).seconds
        order['wait_minutes'] = "{}.{}".format((deltaseconds/60),
            str(deltaseconds % 60).zfill(2))
    return jsonify({"orders": orders}), 200

@app.route('/api/v1/orders/<int:order_id>', methods=['DELETE'])
@basic_auth.required
def remove_order(order_id):
    """Enables caterer to remove a particular order."""
    if(DB.delete_order(order_id)):
        return make_response("The order has been successfully removed", 202)
    return make_response("Please enter a valid meal option", 404)

@app.route('/api/v1/menu')
def get_menu():
    """Returns the menu"""
    return jsonify({"MENU":new_menu }), 200
    
@app.route('/api/v1/menu', methods=["post"])
@basic_auth.required
def setup_menu():
    """Enables caterer to setup menu"""
    data =request.get_json()
    meal_name = data['meal_name']
    day = data['day']
    price = data['price']
    DB.setup_menu(meal_name, day, price)
    return jsonify({"MENU": new_menu}), 201

if __name__ == "__main__":
    app.run(debug=True)
