import datetime
import re
from flasgger import Swagger
from flask import request, jsonify, make_response, json

from .models.user import User
from .models.menu import Menu
from .models.meal import Meal
from .models.order import Order

from . import app, PH
from . import authentication
from .decorators import login_required


auth = authentication.Token()

Swagger(app)
users = User()
meals2 = Meal()
menus = Menu(meals2)
orders2 = Order(menus)


@app.route("/")
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


@app.route("/api/v1/auth/signup", methods=["POST"])
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
    email = data["email"]
    password = data["password"]
    if not User.validate_email_and_password(email, password):
        return make_response("Email or password Invalid", 400)
    salt = PH.get_salt()
    hashed = PH.get_hash(str(password) + str(salt))
    new_user = users.add_user(email, salt, hashed)
    if new_user:
        return make_response("You are now registered", 201)
    return make_response("User already exists", 400)


@app.route("/api/v1/auth/login", methods=["POST"])
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
    email = data["email"]
    password = data["password"]
    if not User.validate_email_and_password(email, password):
        return make_response("Email or password Invalid", 400)
    return users.verify_login(email, password)


@app.route("/api/v1/meals", methods=["GET"])
@login_required
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
    meals = meals2.get_meals()
    return make_response(jsonify({"Meals": meals}), 200)


@app.route("/api/v1/meals/<int:id>", methods=["GET"])
@login_required
def get_meal(id):
    print("j")
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

    meals = meals2.get_meal(id)
    return make_response(jsonify({"Meal": meals}), 200)


@app.route("/api/v1/meals", methods=["POST"])
@login_required
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
    data = request.get_json()
    meal_name = data["meal_name"]
    price = data["price"]
    return meals2.create_meal(meal_name, price)


@app.route("/api/v1/meals/<int:meal_id>", methods=["PUT"])
@login_required
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
    data = request.get_json()
    meal_name = data["meal_name"]
    price = data["price"]
    return meals2.account_update_meal(meal_id, meal_name, price)


@app.route("/api/v1/meals/<int:meal_id>", methods=["DELETE"])
@login_required
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
    return meals2.account_delete_meal(meal_id)


@app.route("/api/v1/orders", methods=['POST'])
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
    data = request.get_json()
    meal_id = data["meal_id"]
    # return orders2.new_order(meal_id)
    return orders2.add_order(meal_id, time=datetime.datetime.utcnow())


@app.route("/api/v1/orders")
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
    return orders2.get_all_orders()


@app.route("/api/v1/orders/<int:id>")
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
    order = orders2.get_order(id)
    return jsonify({"order": order}), 200


@app.route("/api/v1/menu")
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
    return menus.account_get_menu()


@app.route("/api/v1/menu", methods=["post"])
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
    data = request.get_json()
    meal_id = data["meal_id"]
    return menus.account_setup_menu(meal_id)
