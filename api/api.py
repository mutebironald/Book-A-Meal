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
        """Starting point of the API"""
        return "Welcome to Book-A-Meal."

    @app.route("/api/v1/meals")
    @login_required
    def account_get_meals():
        return Meal.get_meals()

    @app.route("/api/v1/meals/<int:id>", methods=["GET"])
    @login_required
    def account_get_specific_meal(id):
        return Meal.get_meal(id)

    @app.route("/api/v1/meals", methods=["POST"])
    @login_required
    def account_create_meal():
    
        data = request.data

        name = data["name"]
        price = data["price"]
        return Meal.create_meal(name, price)

    @app.route("/api/v1/meals/<int:id>", methods=["PUT"])
    def account_update_meal(id):
        name = request.data["name"]
        price = request.data["price"]
        return Meal.update_meal(id, name, price)
     
    @app.route("/api/v1/meals/<int:id>", methods=["DELETE"])
    def account_delete_meal(id):
        return Meal.delete_meal(id)

    @app.route("/api/v1/menu")
    def get_menu():
        return Menu.get_menu()

    @app.route("/api/v1/menu", methods=["POST"])
    def setup_menu():
        data = request.data
        id = data['meal_id']
        if id:
            return Menu.setup_menu(id)

    @app.route("/api/v1/orders")
    def get_all_orders():
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
