from datetime import datetime, timedelta
from flask import jsonify, make_response

from app.__init__ import db, secret
from datetime import datetime

from app import db



class Menu(db.Model):
    """Defines the 'Menu' model mapped to table 'menu'."""
    id = db.Column(db.Integer, primary_key=True)
    meal_id = db.Column(db.Integer, db.ForeignKey('meal.id'))
    day = db.Column(db.DateTime, default=datetime.datetime.today())
    orders = db.relationship('Order', backref='menu')

    def __init__(self, meal_id):
        """Initialises the menu model"""
        self.meal_id = meal_id

    def save(self):
        """Saves items to the menu table"""
        self.day = datetime.datetime.today()
        db.session.add(self)
        try:
            db.session.commit()
        except BaseException:
            db.session.rollback()

    @staticmethod
    def get_menu():
        """Retrieves all the menu items"""
        menus = Menu.query.all()
        if not menus:
            return make_response("No menu present", 400)
        results = []
        for menu in menus:
            obj = {
                'id': menu.id,
                'name': menu.meal.name,
                'price': menu.meal.price,
                'day': menu.day
            }
            results.append(obj)
        response = jsonify(results)
        response.status_code = 200
        return response

    @staticmethod
    def setup_menu(id):
        menu = Menu(meal_id=id)
        menu.save()
        return make_response(
            {"MENU": {
                'id': menu.id,
                'name': menu.meal.name,
                'price': menu.meal.price,
                'day': datetime.datetime.utcnow()
            }
            }), 201

    def __repr__(self):
        return "Menu (%d,%s, %s, %s, %s )" % (
            self.id, self.name, self.meal_id, self.day)
