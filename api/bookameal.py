from flask import  request, jsonify, make_response, json
# from flask_login import  login_user, logout_user, current_user
from .classes.mockdbhelper import Users, Meals, Menu, Orders
from .classes.user import User
from . import app, PH, basic_auth
# from . import login_manager
import datetime
import re
from flasgger import Swagger

Swagger(app)

# @login_manager.user_loader
# def load_user(user_id):
#     user_password = DB.get_user(user_id)
#     if user_password:
#         return User(user_id)

@app.route('/')
def home():
    """
    Home/welcome
    ---
    tags:
      - Welcoming our users
    responses:
        200:
            description: A welcome message appears 
    """
    return "Welcome to Book-A-Meal"

users= Users()

@app.route('/api/v1/auth/signup', methods=["POST"])
def register():
    """
    SignUp route
    ---
    tags:
      - Book-A-Meal API
    parameters:
      - name: email
        in: query
        type: string
        required: true
        description: your email address
      - name: Password
        in: query
        type: string
        required: true
        description: your password
    responses:
        201:
            description: Successfull registration of user
        401:
            description: Unsuccessful user registration
        202:
            description: Double signup rejection

    """
    """Facilitates user registration"""
    data = request.get_json()
    email = data['email']
    if not re.match(r"([\w\.-]+)@([\w\.-]+)(\.[\w\.]+$)", email):
        return jsonify({"error": "Invalid email."}), 400
    password = data['password']
    if password.strip() == "":
        return make_response("You must enter a password", 400)
    if len(password) < 5:
        return jsonify({"message": "Password too short"})
    if users.get_user(email):
        return make_response("The email already exists", 409)
    salt = PH.get_salt()
    hashed = PH.get_hash(str(password) + str(salt))
    users.add_user(email, salt, hashed)
    return make_response("You are now registered", 201)
    
@app.route('/api/v1/auth/login', methods=['POST'])
def login():
    """
    Login route
    ---
    tags:
      - Book-A-Meal API
    parameters:
      - name: email
        in: query
        type: string
        required: true
        description: your email address
      - name: Password
        in: query
        type: string
        required: true
        description: your password
    responses:
        200:
            description: A successfully logged user 
        401:
            description: A user with wrong log inexistent email is informed
        400:
            description: A user trying to gain access without either an email or password
    """
    """Facilitates user registration."""
    data = request.get_json()
    email = data['email']
    if email:
        password = data['password']
        if password:
            stored_user = users.get_user(email)
            print(stored_user)
            if stored_user and PH.validate_password(password, stored_user['salt'], stored_user['hashed']):
                return make_response("success!!, you are now logged in", 200)
            return make_response("Your email does not exist", 401)
        return make_response("You must enter a password", 400)
    return make_response("Your email field is empty", 400)

meals2 = Meals()
@app.route('/api/v1/meals')
@basic_auth.required
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
      200:
        description: Meals present are successfully returned
    """
    """Enables meal retrieval for authenticated user""" 
    meals = meals2.get_meals()
    return make_response(jsonify({'Meals': meals}), 200)


@app.route('/api/v1/meals', methods=['POST'])
@basic_auth.required
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
    200:
      description: Meal is successfully created
    400:
      description: No mealname or price
  """
  """Enables meal retrieval for authenticated user""" 

  """Enables Authenticated user to create meals"""
  data = request.get_json()
  meal_name = data['meal_name']
  price = data['price']
  if meal_name and price:
    meals2.add_meal(meal_name, price)
    return make_response("You successfully created a meal", 200)
  else:
      return make_response('Please enter a meal_name and price', 400)

@app.route('/api/v1/meals/<meal_id>', methods=["PUT"])
@basic_auth.required
def account_update_meal(meal_id):
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
        description: The specified Meal has been updated
      400:
        description: The user tries updating without a meal name 
    """
    """Enables meal retrieval for authenticated user""" 
    """Authenticated user is able to update meal"""
    data = request.get_json()
    meal_name = data['meal_name']
    price = data['price']
    if meal_name:
        meals2.update_meal(meal_id, meal_name, price)
        update = meals2.get_meal(meal_id)
        return jsonify({'meal': update}), 200

    else:
        return make_response('Please enter a meal name', 400)

@app.route('/api/v1/meals/<int:meal_id>', methods=["DELETE"])
@basic_auth.required
def account_delete_meal(meal_id):
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
      202:
        description: The meal has been deleted
    """
    """Authenticated user is able to delete particular meal"""
    meal = meals2.delete_meal(meal_id)
    if meal:
      return make_response("The meal has been deleted", 202)
    else:
      return make_response("The meal specified is not present")

orders2 = Orders()
@app.route('/api/v1/orders', methods=['POST'])
@basic_auth.required
def new_order():
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
        description: order received
    """
    """Enables customer to make an order"""
    data = request.get_json()
    meal_id = data["meal_id"]
    #meal_name = data['meal_name']
    print(orders2)
    orders2.add_order(meal_id, datetime.datetime.utcnow())
    print(orders2)
    return "Your order has been logged and a you will be served shortly"

@app.route('/api/v1/orders')
@basic_auth.required
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
        description: orders retrieved successfully
    """
    """Enables Authenticated caterer is able to get all orders""" 
    now = datetime.datetime.utcnow()
    orders = orders2.get_orders()
    for order in orders:
        deltaseconds = (now - order['time']).seconds
        order['wait_minutes'] = "{}.{}".format((deltaseconds/60),
            str(deltaseconds % 60).zfill(2))
    return jsonify({"orders": orders}), 200

@app.route('/api/v1/orders/<int:id>', methods=['DELETE'])
@basic_auth.required
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
      202:
        description: The order has been successfully removed
      404:
        description: The meal option entered is not valid
    """
    """Enables caterer to remove a particular order."""
    if(orders2.delete_order(id)):
        return make_response("The order has been successfully removed", 202)
    return make_response("Please enter a valid order id", 404)

menus = Menu(meals2) 
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
    responses:
      200:
        description: menu returned successfully
    """
    """Returns the menu"""
    menu = menus.get_menu()
    if menu:
      return jsonify({"MENU":menu }), 
    else:
      return make_response("The menu has not yet been set")
    
@app.route('/api/v1/menu', methods=["post"])
@basic_auth.required
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
        description: Menu successfully created
    """
    """Enables caterer to setup menu"""
    data =request.get_json()
    meal_id = data['meal_id']
    output = menus.setup_menu(meal_id)
    if output:
      return jsonify({"MENU": output}), 201
    else:
      return make_response("Incorrect meal option")

if __name__ == "__main__":
    app.run(debug=True)
