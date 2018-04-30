from flask import Flask, redirect, url_for, request, jsonify
from flask_login import LoginManager
from flask_login import login_required, login_user, logout_user, current_user

from mockdbhelper import MockDBHelper as DBHelper
from mockdbhelper import MOCK_USERS, MOCK_MEALS, MOCK_ORDERS


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
    return "Welcome to Book-A-Meal"
    

@app.route('/api/v1/auth/login', methods=['POST'])
def login():
    #data = request.get_json(force=True)
    #email = data['email']
    #password = data['password']
    email = request.args.get('email')
    password = request.args.get('password')
    stored_user = DB.get_user(email)
    if stored_user and PH.validate_password(password, stored_user['salt'], stored_user['hashed']):
        user = User(email)
        login_user(user)
        return jsonify({"success": "You are now logged in"})
    #return home()


  
    """if email:
        user_password = DB.get_user(email)
        if user_password and user_password == password:
            user = User(email)
            login_user(user, r)
            return redirect(url_for('account'))
        return home()

    else:
        return jsonify({'error':'You are not yet registered'})"""


        
@login_manager.user_loader
def load_user(user_id):
    user_password = DB.get_user(user_id)
    if user_password:
        return User(user_id)

@app.route('/api/v1/auth/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/api/v1/auth/signup', methods=["POST"])
def register():
    email = request.json.get('email')
    pw1 = request.json.get('password')
    pw2 = request.json.get('password2')
    if not pw1 == pw2:
        return redirect(url_for('home'))
    salt = PH.get_salt()
    hashed = PH.get_hash(pw1 + salt)
    DB.add_user(email, salt, hashed)
    return redirect(url_for('home'))


#working route
@app.route('/api/v1/meals')
#@login_required
def account():
    meals = DB.get_meals(current_user.get_id())
    return jsonify({'MOCK_MEALS': meals})

@app.route('/api/v1/meals', methods=['POST'])
#@login_required
def account_createmeal():
    mealname = request.json.get('mealname')
    mealid = DB.add_meal(mealname, current_user.get_id())
    DB.update_meal(mealid, mealname)
    return redirect(url_for('account'))


@app.route('/api/v1/meals/<mealid>', methods=["PUT"])
#@login_required
def account_updatemeal():
    mealid = request.args.get('mealid')
    DB.update_meal(mealid, 'Posho and beans')
    return jsonify({'meals': mealid['mealname'] })




@app.route('/api/v1/meals/<mealid>', methods=["DELETE"])
#@login_required
def account_deletemeal():
    mealid = request.args.get('mealid')
    DB.delete_meal(mealid)
    return redirect(url_for('account'))

#working route
@app.route('/api/v1/orders/<int:order_id', methods=['POST'])
def new_order(order_id):
    DB.add_order(order_id, datetime.datetime.utcnow())
    return "Your order has been logged and a you will be served shortly"



#working route
@app.route('/api/v1/orders')
#@login_required
def get_all_orders():
    now = datetime.datetime.utcnow()
    orders = DB.get_orders(current_user.get_id())
    for order in orders:
        deltaseconds = (now - order['time']).seconds
        order['wait_minutes'] = "{}.{}".format((deltaseconds/60),
            str(deltaseconds % 60).zfill(2))
    return jsonify({"orders": orders})


@app.route('/api/v1/orders/<int:order_id>')
#@login_required
def remove_order():
    order_id = request.args.get("order_id")
    DB.delete_order(order_id)
    return jsonify({"The order has been successfully removed":order_id})
    

if __name__ == "__main__":
    app.run(debug=True)
