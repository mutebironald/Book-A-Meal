import datetime
import re
from flask import make_response, jsonify

from api import PH
from ..authentication import Token


class Menu:
    """A class to represent the Menu of meals for a particular day"""

    def __init__(self, meals):
        """Initialises the Menu class"""
        self.menu = []
        self.meals = meals

    def account_get_menu(self):
        """Implements get meal logic"""
        menu = self.menu
        if menu:
            return jsonify({"MENU": menu}), 200
        else:
            return make_response("The menu has not yet been set"), 404

    def account_setup_menu(self, meal_id):
        """Helps caterer to set the menu for a specific day"""
        meal_get = self.meals.get_meals()
        for meal in meal_get:
            if meal["id"] == int(meal_id):
                self.menu.append(meal)
                return jsonify({"MENU": self.menu}), 201
            else:
                return make_response("Incorrect meal option"), 404
