import datetime
from flask import make_response, jsonify

from api import PH
from ..authentication import Token


class Order:
    """A class to represent a customers/users orders"""

    def __init__(self, menu):
        """Initializes the order class"""
        self.orders = []
        self.menu = menu
        self.id = 1

    # def new_order(self, meal_id):
    #     """Helps in making a new order"""
    #     self.add_order(meal_id, datetime.datetime.utcnow())
    #     return "Your order has been logged and a you will be served shortly"

    def add_order(self, meal_id, time):
        """Enables customer to make an order."""
        # menu_returned = self.menu.account_get_menu()
        menu_returned = self.menu
        print(self.menu)
        for meal in menu_returned:
            if meal["id"] == meal_id:
                self.orders.append({
                    "id": self.id,
                    "meal": meal,
                    "time": time,
                    "cleared": False
                })
                self.id += 1
                # print(self.id)
                # return self.orders
                response = self.orders
                response.status_code = 200
                return make_response(jsonify(response),
                                     "Your order has been logged and a you will be served shortly")

    def get_all_orders(self):
        """Enables caterer to retrieve all orders"""
        now = datetime.datetime.utcnow()
        # orders = self.get_orders()
        orders = self.orders
        for order in orders:
            deltaseconds = (now - order["time"]).seconds
            order["wait_minutes"] = "{}.{}".format(
                (deltaseconds / 60), str(deltaseconds % 60).zfill(2))
            return jsonify({"orders": orders}), 200

    # def get_orders(self):
    #     """Returns all orders belonging to a particular caterer"""
    #     return self.orders

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
