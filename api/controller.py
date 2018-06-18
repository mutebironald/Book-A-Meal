from flask import  request, jsonify, make_response, json
from .classes.models import Users, Meals, Menu, Orders
from .classes.user import User
from . import app, PH
import datetime
import re
from flasgger import Swagger
from . import authentication

auth = authentication.Tokens()
Swagger(app)
users= Users()
meals2 = Meals()
menus = Menu(meals2)
orders2 = Orders(menus)

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

@app.route('/api/v1/auth/signup', methods=["POST"])
def register():
    """
    SignUp route
    ---
    tags:
      - Book-A-Meal API
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - "email"
            - "password"
          properties:
            email:
              type: "string"
              example: "zeroberto@gmail.com"
            password:
              type: "string"
              format: password
              example: "1234567"
    responses:
        201:
            description: Successfull registration of user
            schema:
              type: object
            examples:
              { "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1Mjg1NDc5NzEsInN1YiI6MX0._A9-QMDV1nL7AW5BXAAvqJw3C2E1pNJVcdUSGo2Njs8"}
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
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - "email"
            - "password"
          properties:
            email:
              type: "string"
              example: "zeroberto@gmail.com"
            password:
              type: "string"
              format: password
              example: "1234567"
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
            if stored_user and PH.validate_password(password, stored_user['salt'], stored_user['hashed']):
              access_token = auth.generate_token(stored_user['id'])
              return make_response(jsonify({"token": access_token,
              "message": "success!!, you are now logged in"}), 200)
            return make_response("Your email does not exist", 401)
        return make_response("You must enter a password", 400)
    return make_response("Your email field is empty", 400)

@app.route('/api/v1/meals', methods=["GET"])
def account_get_meals():
  """
    Meals route
    ---
    tags:
      - Book-A-Meal API
    parameters:
      - name: Authorization
        in: header
        required: true
        properties:
          Authorization:
            type: "string"
    responses:
        200:
            description: Meals present are successfully returned
  """  
  """Enables meal retrieval for authenticated user""" 
  access_token = request.headers.get("Authorization")
  if access_token:
    user_id = auth.decode_token(access_token)
    if not isinstance (user_id, str):
      meals = meals2.get_meals()
      return make_response(jsonify({'Meals': meals}), 200)

@app.route('/api/v1/meals/<int:id>', methods=["GET"])
def get_meal(id):
  """
    Meals route
    ---
    tags:
      - Book-A-Meal API
    parameters:
      - name: Authorization
        in: header
        required: true
        properties:
          Authorization:
            type: "string"
      - name: id
        in: path
        required: true
        properties:
          id:
            type: "int"
        default: 1
    responses:
        200:
            description: A successfully returned meal.
  """ 
  
  access_token = request.headers.get("Authorization")
  if access_token:
    user_id = auth.decode_token(access_token)
    if not isinstance (user_id, str):
      meals = meals2.get_meal(id)
      return make_response(jsonify({'Meal': meals}), 200)

@app.route('/api/v1/meals', methods=['POST'])
def account_create_meal():
  """
    Meals route
    ---
    tags:
      - Book-A-Meal API
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - "meal_name"
            - "price"
          properties:
            meal_name:
              type: "string"
              example: "Indian potatoes with Ughali"
            price:
              type: "string"
              example: "6000"
      - name: Authorization
        in: header
        required: true
        properties:
          Authorization:
            type: "string"
            
    responses:
        200:
            description: Meal is successfully returned.
        400:
            description: No mealname or price.
  """  

  """Enables Authenticated user to create meals"""
  access_token = request.headers.get("Authorization")
  if access_token:
    print(access_token)
    user_id = auth.decode_token(access_token)
    if not isinstance (user_id, str):
      data = request.get_json()
      meal_name = data['meal_name']
      price = data['price']
      if meal_name and price:
        meals2.add_meal(meal_name, price)
        return make_response("You successfully created a meal", 200)
      else:
          return make_response('Please enter a meal_name and price', 400)
    return "id is a string"
  return "no access-token"

@app.route('/api/v1/meals/<int:meal_id>', methods=["PUT"])
def account_update_meal(meal_id):
  """
    Meals route
    ---
    tags:
      - Book-A-Meal API
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - "meal_name"
            - "price"
          properties:
            meal_name:
              type: "string"
              example: "Chicken na ketchup"
            price:
              type: "int"
              example: "6000"
      - name: meal_id
        in: path
        required: true
        properties:
          meal_id:
            type: "int"
        default: 1
      - name: Authorization
        in: header
        required: true
        properties:
          Authorization:
            type: "string"
            
    responses:
        200:
            description: The specified meal has been updated.
        400:
            description: The user tries updating without a meal name.
  """  
    
     
  """Authenticated user is able to update meal"""
  access_token = request.headers.get("Authorization")
  if access_token:
    user_id = auth.decode_token(access_token)
    if not isinstance (user_id, str):
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
def account_delete_meal(meal_id):
    """
    Meals route
    ---
    tags:
      - Book-A-Meal API
    parameters:
      - name: meal_id
        in: path
        required: true
        properties:
          meal_id:
            type: "int"
        default: 1
      - name: Authorization
        in: header
        required: true
        properties:
          Authorization:
            type: "string"
    responses:
        202:
            description: The meal has been deleted. 
        
    """

    """Authenticated user is able to delete particular meal"""
    access_token = request.headers.get("Authorization")
    if access_token:
      user_id = auth.decode_token(access_token)
      if not isinstance (user_id, str):
        meal = meals2.delete_meal(meal_id)
        if meal:
          return make_response("The meal has been deleted", 202)
        else:
          return make_response("The meal specified is not present")

@app.route('/api/v1/orders', methods=['POST'])
def new_order():
    """
    Orders route
    ---
    tags:
      - Book-A-Meal API
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - "meal_id"
          properties:
            meal_id:
              type: "string"
              example: "1"
      - name: Authorization
        in: header
        required: true
        properties:
          Authorization:
            type: "string"
            
    responses:
        200:
            description: order received
        
    """  
  
    """Enables customer to make an order"""
    access_token = request.headers.get("Authorization")
    if access_token:
      user_id = auth.decode_token(access_token)
      if not isinstance (user_id, str):
        data = request.get_json()
        meal_id = data["meal_id"]
        orders2.add_order(meal_id, datetime.datetime.utcnow())
        return "Your order has been logged and a you will be served shortly"

@app.route('/api/v1/orders')
def get_all_orders():
    """
    orders route
    ---
    tags:
      - Book-A-Meal API
    parameters:
      - name: Authorization
        in: header
        required: true
        properties:
          Authorization:
            type: "string"
    responses:
        200:
            description: Orders retrieved successfully.
    """  
    
    """Enables Authenticated caterer is able to get all orders""" 
    access_token = request.headers.get("Authorization")
    if access_token:
      user_id = auth.decode_token(access_token)
      if not isinstance (user_id, str):
        now = datetime.datetime.utcnow()
        orders = orders2.get_orders()
        for order in orders:
          deltaseconds = (now - order['time']).seconds
          order['wait_minutes'] = "{}.{}".format((deltaseconds/60),
                str(deltaseconds % 60).zfill(2))
          return jsonify({"orders": orders}), 200
        
@app.route('/api/v1/orders/<int:id>')
def get_order(id):
    """
    Orders route
    ---
    tags:
      - Book-A-Meal API
    parameters:
      - name: Authorization
        in: header
        required: true
        properties:
          Authorization:
            type: "string"
      - name: id
        in: path
        required: true
        properties:
          id:
            type: "int"
        default: 1
    responses:
        200:
            description: Orders retrieved successfully.
    """  
    """Enables caterer to remove a particular order."""
    access_token = request.headers.get("Authorization")
    if access_token:
      user_id = auth.decode_token(access_token)
      if not isinstance (user_id, str):
        order = orders2.get_order(id)
        print(order)
        return jsonify({"order": order}), 200
      
@app.route('/api/v1/menu')
def get_menu():
    """
    Menu route
    ---
    tags:
      - Book-A-Meal API
    parameters:
      - name: Authorization
        in: header
        required: true
        properties:
          Authorization:
            type: "string"
    responses:
        200:
            description: Menu retrieved successfully.
        404:
            description: The menu has not been set.
    """  
    """Returns the menu"""
    access_token = request.headers.get("Authorization")
    if access_token:
      user_id = auth.decode_token(access_token)
      if not isinstance (user_id, str):
        menu = menus.get_menu()
        if menu:
          return jsonify({"MENU":menu }), 200
        else:
          return make_response("The menu has not yet been set"), 404
    
@app.route('/api/v1/menu', methods=["post"])
def setup_menu():
    """
    Menu route
    ---
    tags:
      - Book-A-Meal API
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - "meal_id"
          properties:
            meal_id:
              type: "string"
              example: "1"
      - name: Authorization
        in: header
        required: true
        properties:
          Authorization:
            type: "string"
            
    responses:
        201:
            description: Menu successfully created.
    """  
   
    """Enables caterer to setup menu"""
    access_token = request.headers.get("Authorization")
    if access_token:
      user_id = auth.decode_token(access_token)
      if not isinstance (user_id, str):
        data =request.get_json()
        meal_id = data['meal_id']
        output = menus.setup_menu(meal_id)
        print(output)
        if output:
          return jsonify({"MENU": output}), 201
        else:
          return make_response("Incorrect meal option"), 404
  
if __name__ == "__main__":
    app.run(debug=True)
