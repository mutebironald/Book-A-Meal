from flask import Flask, redirect, url_for, request, jsonify, make_response, json
from flask_login import LoginManager
from flask_login import login_required, login_user, logout_user, current_user

from mockdbhelper import MockDBHelper as DBHelper
from mockdbhelper import MOCK_USERS, MOCK_MEALS, MOCK_ORDERS, MOCK_MENUS


from user import User
import os, binascii

import datetime

from passwordhelper import PasswordHelper


app = Flask(__name__)
app.secret_key = binascii.hexlify(os.urandom(24))
login_manager = LoginManager(app)

PH = PasswordHelper()


DB = DBHelper()

@app.route('/')
def home():
    """Starting point for the API"""
    return "Welcome to Book-A-Meal"

@app.route('/api/v1/auth/signup', methods=["POST"])
def register():
    """Facilitates user registration"""
    email = request.form.get('email')
    pw1 = request.form.get('password')
    pw2 = request.form.get('password2')
    if not pw1 == pw2:
        return make_response("Your password or email is incorrect", 401)
    salt = PH.get_salt()
    hashed = PH.get_hash(pw1 + salt)
    DB.add_user(email, salt, hashed)
    return make_response("You are now registered", 201)
    

@app.route('/api/v1/auth/login', methods=['POST'])
def login():
    """Facilitates user registration."""
    email = request.form.get('email')
    password = request.form.get('password')
    stored_user = DB.get_user(email)
    print(stored_user)
    if stored_user and PH.validate_password(password, stored_user['salt'], stored_user['hashed']):
        user = User(email)
        login_user(user)
        return make_response("success!!, you are now logged in", 200)
    return make_response("Your email does not exist", 401)


        
@login_manager.user_loader
def load_user(user_id):
    user_password = DB.get_user(user_id)
    if user_password:
        return User(user_id)

@app.route('/api/v1/auth/logout')
def logout():
    """signs out loged in user"""
    logout_user()
    return make_response("You are now logged out", 200)

@app.route('/api/v1/meals')
@login_required
def account():
    """Enables meal retrieval for authenticated user"""
    meals = DB.get_meals(current_user.get_id())
    return jsonify({'MOCK_MEALS': meals})

@app.route('/api/v1/meals', methods=['POST'])
#@login_required
def account_createmeal():
    """Enables Authenticated user to create meals"""
    meal_name = request.form.get('meal_name')
    meal_id = DB.add_meal(meal_name, current_user.get_id())
    DB.update_meal(meal_id, meal_name)
    return make_response("You successfully created a meal", 200)



@app.route('/api/v1/meals/<meal_id>', methods=["PUT"])
#@login_required
def account_updatemeal(meal_id):
    """Authenticated user is ale to update meal"""
    meal_name = request.form.get('mealname')
    DB.update_meal(meal_id, meal_name)
    return jsonify({'meals': MOCK_MEALS})




@app.route('/api/v1/meals/<meal_id>', methods=["DELETE"])
#@login_required
def account_deletemeal(meal_id):
    """Authenticated user is able to delete particular meal"""
    meal_id = request.form.get('meal_id')
    DB.delete_meal(meal_id)
    return make_response("The meal has been deleted", 202)


#verify
@app.route('/api/v1/orders/<meal_id>', methods=['POST'])
def new_order(meal_id):
    """Enables customer to make an order"""
    DB.add_order(meal_id, datetime.datetime.utcnow())
    return "Your order has been logged and a you will be served shortly"


#okay
@app.route('/api/v1/orders')
#@login_required
def get_all_orders():
    """Enables Authenticated caterer is able to get all orders""" 
    now = datetime.datetime.utcnow()
    orders = DB.get_orders(current_user.get_id())
    for order in orders:
        deltaseconds = (now - order['time']).seconds
        order['wait_minutes'] = "{}.{}".format((deltaseconds/60),
            str(deltaseconds % 60).zfill(2))
    return jsonify({"orders": orders})


#verify
@app.route('/api/v1/orders/<order_id>')
#@login_required
def remove_order(order_id):
    """Enables caterer to remove a particular order."""
    order_id = request.args.get("order_id")
    DB.delete_order(order_id)
    return make_response("The order has been successfully removed", 202)


    

#menu.........
#POST /menu/  setup the menu for the day
#GET /menu/  Get the menu for the day

@app.route('/api/v1/menu')
def get_menu():
    """Returns the menu"""
    return jsonify({"MENU": MOCK_MENUS })

@app.route('/api/v1/menu', methods=["post"])
def setup_menu():
    """Enables caterer to setup menu"""
    meal_name = request.form.get('meal_name')
    meal_id = request.form.get('meal_id')
    DB.setup_menu(meal_id, meal_name)
    return jsonify({"MENU": MOCK_MENUS})



if __name__ == "__main__":
    app.run(debug=True)
