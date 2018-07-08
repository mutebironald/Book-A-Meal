import datetime
import re
from flask import make_response, jsonify

from api import PH
from ..authentication import Token


class User:
    """A class for all users"""

    def __init__(self):
        """Initialises the user class"""
        self.users = []
        self.id = 1

    def get_user(self, email):
        """Retrieves a user from a list of users"""
        available_user = [
            user for user in self.users if user["email"] == email]
        if available_user:
            return available_user[0]
        return False

    def verify_login(self, email, password):
        """validates login details"""
        response_message = "You are now logged in"
        response_code = 200
        absent_code = 401
        stored_user = self.get_user(email)
        if stored_user and PH.validate_password(
                password, stored_user["salt"], stored_user["hashed"]):
            access_token = Token().generate_token(stored_user["id"])
            return make_response(
                jsonify({"token": access_token, "message": response_message}), response_code)
        return make_response("Please register then login", absent_code)

    @staticmethod
    def validate_email_and_password(email, password):
        """Ensures signup with correct credentials"""
        if not re.match(r"([\w\.-]+)@([\w\.-]+)(\.[\w\.]+$)", email):
            return False
        if password.strip() == "":
            return False
        if len(password) < 5:
            return False
        return True

    def add_user(self, email, salt, hashed):
        """Helps add a user to the list of users"""
        if self.get_user(email):
            return False
        new_user = {
            "id": self.id,
            "email": email,
            "salt": salt,
            "hashed": hashed}
        self.users.append(new_user)
        self.id += 1
        return new_user


class Meal:
    """A class to represent the meals"""

    def __init__(self):
        """Initialises the meal class"""
        self.meals = []
        self.id = 1

    def account_update_meal(self, meal_id, meal_name, price):
        """Implements the update meal logic"""
        if isinstance(price, int) and meal_name:
            self.update_meal(meal_id, meal_name, price)
            update = self.get_meal(meal_id)
            return jsonify({"meal": update}), 200
        else:
            return make_response("Enter a valid meal name and price", 400)

    def add_meal(self, meal_name, price):
        """Enables caterer to add a meal option"""
        self.meals.append({
            "id": self.id,
            "meal_name": meal_name,
            "price": price
        })
        self.id += 1
        return meal_name

    def create_meal(self, meal_name, price):
        """Enables meal creation"""
        if isinstance(price, int) and meal_name:
            self.add_meal(meal_name, price)
            return make_response("You successfully created a meal", 200)
        else:
            return make_response("Enter a valid meal name and price", 400)

    def update_meal(self, _id, meal_name, price):
        """Enables caterer to change a specific meal option"""
        for meal in self.meals:
            if meal["id"] == _id:
                meal["meal_name"] = meal_name
                meal["price"] = price
                break

    def get_meals(self):
        """Returns all available meal options"""
        return self.meals

    def get_meal(self, meal_id):
        """To get meals from meal options"""
        for meal in self.meals:
            if meal["id"] == meal_id:
                return meal

    def delete_meal(self, meal_id):
        """Enables the caterer to resolve/remove meal options"""
        c = 0
        for meal in self.meals:
            if meal["id"] == meal_id:
                del self.meals[c]
                return True
            c += 1

    def account_delete_meal(self, meal_id):
        """Enables meal deletion"""
        meal = self.delete_meal(meal_id)
        if meal:
            return make_response("The meal has been deleted", 202)
        else:
            return make_response("The meal specified is not present", 400)


class Menu:
    """A class to represent the Menu of meals for a particular day"""

    def __init__(self, meals):
        """Initialises the Menu class"""
        self.menu = []
        self.meals = meals

    def get_menu(self):
        """Enables menu retrieval"""
        return self.menu

    def account_get_menu(self):
        """Implements get meal logic"""
        menu = self.get_menu()
        if menu:
            return jsonify({"MENU": menu}), 200
        else:
            return make_response("The menu has not yet been set"), 404

    def account_setup_menu(self, meal_id):
        """Helps caterer to set the menu for a specific day"""
        output = self.setup_menu(meal_id)
        if output:
            return jsonify({"MENU": output}), 201
        else:
            return make_response("Incorrect meal option"), 404

    def setup_menu(self, meal_id):
        """Implements menu creation"""
        meal_get = self.meals.get_meals()
        for meal in meal_get:
            if meal["id"] == int(meal_id):
                self.menu.append(meal)
                return self.menu
            else:
                return False


class Order:
    """A class to represent a customers/users orders"""

    def __init__(self, menu):
        """Initializes the order class"""
        self.orders = []
        self.menu = menu
        self.id = 1

    def new_order(self, meal_id):
        """Helps in making a new order"""
        self.add_order(meal_id, datetime.datetime.utcnow())
        return "Your order has been logged and a you will be served shortly"

    def add_order(self, meal_id, time):
        """Enables customer to make an order."""
        menu_returned = self.menu.get_menu()
        for meal in menu_returned:
            if meal["id"] == int(meal_id):
                self.orders.append({
                    "id": self.id,
                    "meal": meal,
                    "time": time,
                    "cleared": False
                })
                self.id += 1
                print(self.id)
                return self.orders

    def get_all_orders(self):
        """Enables caterer to retrieve all orders"""
        now = datetime.datetime.utcnow()
        orders = self.get_orders()
        for order in orders:
            deltaseconds = (now - order["time"]).seconds
            order["wait_minutes"] = "{}.{}".format(
                (deltaseconds / 60), str(deltaseconds % 60).zfill(2))
            return jsonify({"orders": orders}), 200

    def get_orders(self):
        """Returns all orders belonging to a particular caterer"""
        return self.orders

    def get_order(self, order_id):
        for order in self.orders:
            if order["id"] == order_id:
                return order

    def delete_order(self, order_id):
        """Enables the caterer to resolve/remove orders"""
        c = 0
        for order in self.orders:
            if order["id"] == order_id:
                del self.orders[c]
                return True
            c += 1
