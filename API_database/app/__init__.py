from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from flask import request, jsonify, abort, make_response

import os
import binascii

from instance.config import app_config


db = SQLAlchemy()
secret = binascii.hexlify(os.urandom(24))


def create_app(config_name):
    from app.model.user import User
    from app.model.meal import Meal
    from app.model.menu import Menu
    from app.model.order import Order

    from app.decorators import login_required

    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile("config.py")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = secret
    with app.app_context():
        db.init_app(app)
        db.create_all()

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

        """Starting point of the API"""
        return "Welcome to Book-A-Meal."

    @app.route("/api/v1/meals")
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
            400:
                description: No meals present
            200:
                description: Meals are present
        """
        return Meal.get_meals()

    @app.route("/api/v1/meals/<int:id>", methods=["GET"])
    @login_required
    def account_get_specific_meal(id):
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
            400:
                description: The meal with the specified id is absent
            200:
                description: The meal is successfully returned.
        """
        return Meal.get_meal(id)

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
                description: The meal has been created.
        """
        data = request.data

        name = data["name"]
        price = data["price"]
        return Meal.create_meal(name, price)

    @app.route("/api/v1/meals/<int:id>", methods=["PUT"])
    def account_update_meal(id):
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
            404:
                description: The meal you want to update is not in the database.
            200:
                description: The meal has been successfully updated.
        """
        name = request.data["name"]
        price = request.data["price"]
        return Meal.update_meal(id, name, price)

    @app.route("/api/v1/meals/<int:id>", methods=["DELETE"])
    def account_delete_meal(id):
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
            200:
                description: The meal with the ID specified has been deleted

        """

        return Meal.delete_meal(id)

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
            400:
                description: There is no menu present.
            200:
                description: The menu has successfully been returned.
        """
        return Menu.get_menu()

    @app.route("/api/v1/menu", methods=["POST"])
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
                description: The menu has been successfully returned.
        """
        data = request.data
        id = data['meal_id']
        if id:
            return Menu.setup_menu(id)

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
                description: Successfully returned all the orders present.
            400:
                description: No orders present at the moment.
        """
        orders = Order.get_all_orders()
        if orders:
            results = []
            for order in orders:
                obj = {
                    "id": order.id,
                    "order_time": order.order_time
                }
                results.append(obj)
            response = jsonify(results)
            response.status_code = 200
            return response
        else:
            return make_response("No orders present", 400)

    @app.route("/api/v1/orders/<int:id>", methods=["DELETE"])
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
        order = Order.query.filter_by(id=id).first()
        if not order:
            return make_response(
                "The order specified is not present"), 400
        Order.session.delete(order)
        response = make_response(
            "The order has been deleted", 200)
        return response

    from .auth import auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app
