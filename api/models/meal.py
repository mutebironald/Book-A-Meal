from flask import make_response, jsonify


class Meal:
    """A class to represent the meals"""

    def __init__(self):
        """Initialises the meal class"""
        self.meals = []
        self.id = 1

    def account_update_meal(self, meal_id, meal_name, price):
        """Implements the update meal logic"""
        if isinstance(price, int):
            for meal in self.meals:
                if meal["id"] == meal_id:
                    meal["meal_name"] = meal_name
                    meal["price"] = price
                    break

            update = self.get_meal(meal_id)
            return jsonify({"meal": update}), 200
        else:
            return make_response("Enter a valid meal name and price", 400)

    def create_meal(self, meal_name, price):
        """Enables meal creation"""

        try:
            price = int(price)
        except ValueError:
            return make_response("Enter a valid meal name and price", 400)
        else:
            self.meals.append({
                "id": self.id,
                "meal_name": meal_name,
                "price": price
            })
            self.id += 1
            response = jsonify(self.meals)
            response.status_code = 201
            return make_response(response, "You successfully created a meal")

    def get_meals(self):
        """Returns all available meal options"""
        return self.meals

    def get_meal(self, meal_id):
        """To get meals from meal options"""
        for meal in self.meals:
            if meal["id"] == meal_id:
                return meal

    def account_delete_meal(self, meal_id):
        """Enables meal deletion"""
        c = 0
        for meal in self.meals:
            if meal["id"] == meal_id:
                del self.meals[c]
                return make_response("The meal has been deleted", 202)
            c += 1
        return make_response("The meal specified is not present", 400)
