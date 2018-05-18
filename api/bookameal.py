from flask import  request, jsonify, make_response, json
from flask_login import  login_user, logout_user, current_user
from .classes.mockdbhelper import MOCK_USERS, MOCK_MEALS, MOCK_ORDERS, MOCK_MENUS
from .classes.user import User
from . import app, PH, DB, basic_auth
from . import login_manager
import datetime

from validate_email_address import validate_email
from itsdangerous import URLSafeTimedSerializer


@login_manager.user_loader
def load_user(user_id):
    user_password = DB.get_user(user_id)
    if user_password:
        return User(user_id)

@app.route('/')
def home():
    """Starting point for the API"""
    return "Welcome to Book-A-Meal"

@app.route('/api/v1/auth/signup', methods=["POST"])
def register():
    """Facilitates user registration"""
    email = request.form.get('email')
    email = validate_email(email)
    if email:
        password = request.form.get('password')
        if password:
            if DB.get_user(email):
                return make_response("The email already exists", 409)
            salt = PH.get_salt()
            hashed = PH.get_hash(password + str(salt))
            DB.add_user(email, salt, hashed)
            return make_response("You are now registered", 201)
        return make_response("You must enter a password", 400)
    # return make_response("Your email field is empty", 400)
    return make_response("please enter a valid email address", 400)
    
@app.route('/api/v1/auth/login', methods=['POST'])
def login():
    """Facilitates user registration."""
    email = request.form.get('email')
    if email:
        password = request.form.get('password')
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
    meal_name = request.form.get('meal_name')
    price = request.form.get('price')
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
    meal_name = request.form.get('meal_name')
    price = request.form.get('price')
    if meal_name:
        DB.update_meal(meal_id, meal_name, price)
        return jsonify({'meals': MOCK_MEALS}), 200

    else:
        return make_response('Please enter a meal name', 400)

@app.route('/api/v1/meals/<meal_id>', methods=["DELETE"])
@basic_auth.required
def account_delete_meal(meal_id):
    """Authenticated user is able to delete particular meal"""
    meal_id = request.form.get('meal_id')
    DB.delete_meal(meal_id)
    return make_response("The meal has been deleted", 202)

@app.route('/api/v1/orders/<int:meal_id>', methods=['POST'])
def new_order(meal_id):
    """Enables customer to make an order"""
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
    return jsonify({"MENU": MOCK_MENUS }), 200
    
@app.route('/api/v1/menu', methods=["post"])
@basic_auth.required
def setup_menu():
    """Enables caterer to setup menu"""
    meal_name = request.form.get('meal_name')
    meal_id = request.form.get('meal_id')
    DB.setup_menu(meal_id, meal_name)
    return jsonify({"MENU": MOCK_MENUS}), 201

if __name__ == "__main__":
    app.run(debug=True)
