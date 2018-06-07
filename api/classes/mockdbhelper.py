import datetime

class Users:
    """A class for all users"""
    
    def __init__(self):
        self.users = []
        self.id = 1


    def get_user(self, email):
        """Helps am already registered user to log in."""
        available_user = [user for user in self.users if user["email"] == email]
        if available_user:
            return available_user[0]
        return None

    def add_user(self, email, salt, hashed):
        """Enables user registration or signup"""
        self.users.append({
            "id": self.id , 
            "email" : email, 
            "salt": salt,
            "hashed":hashed
            })
        self.id += 1

class Meals:
    """A class to represent the meals"""
    def __init__(self):
        self.meals = []
        self.id = 1

    def add_meal(self, meal_name, price):
        """Enables caterer to add a meal option"""
        self.meals.append({
            "id": self.id,
            'meal_name': meal_name,
            'price': price
            })
        self.id += 1
        return meal_name
    
    def update_meal(self, _id, meal_name, price):
        """Enables caterer to change a specific meal option"""
        for meal in self.meals:
            if u"{}".format(meal.get('id')) == _id:
                meal['meal_name'] = meal_name
                meal['price'] = price
                break
    
    def get_meals(self):
        """Returns all available meal options"""
        return self.meals

    def get_meal(self, meal_id):
        """To get meals from meal options"""
        for meal in self.meals:
            if u"{}".format(meal.get('id')) == meal_id:
                return meal

    def delete_meal( self, meal_id):
        """Enables the caterer to resolve/remove orders"""
        meal = [(i, meal) for i, meal in enumerate(self.meals) if meal['id'] == meal_id]
        if meal:
            self.meals.remove(self.meals[meal[0][0]])
            return True
        else:
            return False

class Menu:
    """A class to represent the Menu of meals for a particular day"""
    def __init__(self):
        self.menus = []
        self.id = 1

    def get_menu(self):
        for menu in self.menus:
            return menu

    def setup_menu(self, meal_name, price):
        self.menus.append(
                {
                    'name': meal_name,
                    'price': price
                }
        )
        self.id =+ 1
        return self.menus

meals = Meals()
class Orders:
    """A class to represent a customers/users orders"""
    def __init__(self, ):
        self.orders = []
        self.id = 1

    def add_order(self, meal_id, time):
        """Enables customer to make an order."""
        self.orders.append({ 
            "meal": meals.get_meal(meal_id), 
            "time": time,
            "cleared": False
            })
        self.id =+ 1
        return self.orders
        
    
    def get_orders(self):
        """Returns all orders belonging to a particular caterer"""
        return self.orders

    def delete_order( self, order_id):
        """Enables the caterer to resolve/remove orders"""
        order = [(i, order) for i, order in enumerate(self.orders) if order['id'] == order_id]
        if order:
            self.orders.remove(self.orders[order[0][0]])
            return True
        return False


# class MockDBHelper:
#     """
#     This class handles all methods associated
#     with the user, meals, menu and order.
#     """

    # def get_user(self, email):
    #     """Helps am already registered user to log in."""
    #     available_user = [user for user in MOCK_USERS if user["email"] == email]
    #     print(available_user)
    #     if available_user:
    #         return available_user[0]
    #     return None

    # def add_user(self, email, salt, hashed):
    #     """Enables user registration or signup"""
    #     MOCK_USERS.append({
    #         "email" : email, 
    #         "salt": salt,
    #         "hashed":hashed
    #         })

    # def add_meal(self, meal_name, price,  owner):
    #     """Enables caterer to add a meal option"""
    #     MOCK_MEALS.append({
    #         '_id': MOCK_MEALS[-1]['_id'] + 1 ,
    #         'meal_name': meal_name,
    #         'price': price
    #         })

    #     return meal_name

    # def update_meal(self, _id, meal_name, price):
    #     """Enables caterer to change a specific meal option"""
    #     for meal in MOCK_MEALS:
    #         if u"{}".format(meal.get('_id')) == _id:
    #             meal['meal_name'] = meal_name
    #             meal['price'] = price
    #             break
           
    # def get_meals(self, owner_id):
    #     """Returns all available meal options"""
    #     for meal in MOCK_MEALS:
    #         if meal.get("owner_id") == owner_id:
    #             return MOCK_MEALS
    #         break

    # def get_meal(self, meal_id):
    #     """To get meals from meal options"""
    #     for meal in MOCK_MEALS:
    #         if u"{}".format(meal.get('_id')) == meal_id:
    #             return meal

    # def delete_meal( self, meal_id):
    #     """Enables the caterer to resolve/remove orders"""
    #     meal = [(i, meal) for i, meal in enumerate(MOCK_MEALS) if meal['_id'] == meal_id]
    #     if meal:
    #         print(MOCK_MEALS[meal[0][0]])
    #         MOCK_MEALS.remove(MOCK_MEALS[meal[0][0]])
    #         print(meal)
    #         return True
    #     else:
    #         return False

    # def add_order(self, meal_id, time):
    #     """Enables customer to make an order."""
    #     meal = self.get_menu(meal_id)
    #     if meal:
    #         MOCK_ORDERS.append({
    #             '_id':MOCK_ORDERS[-1]['_id'] + 1, 
    #             "meal_name": meal["meal_name"], 
    #             "meal_id": meal_id, 
    #             "time": time
    #             })
    #         return True
    #     else:
    #         return False
    
    # def get_orders(self, owner_id):
    #     """Returns all orders belonging to a particular caterer"""
    #     return MOCK_ORDERS

    # def delete_order( self, order_id):
    #     """Enables the caterer to resolve/remove orders"""
    #     order = [(i, order) for i, order in enumerate(MOCK_ORDERS) if order['_id'] == order_id]
    #     if order:
    #         MOCK_ORDERS.remove(MOCK_ORDERS[order[0][0]])
    #         return True
    #     return False
        
    # def get_menu(self, day):
    #     for menu in new_menu:
    #         if menu['day'] == day:
    #             return menu

    # def setup_menu(self, meal_name, day, price):
    #     new_menu.append(
    #         {
    #             'day': day,
    #             'meal': {
    #                 'name': meal_name,
    #                 'price': price
    #             }
    #         }
    #     )
    #     return new_menu

    # def setup_menu(self, meal_id, meal_name):
    #     """Enables caterer to setup menu for the day"""
    #     MOCK_MENUS.append({"_id": MOCK_MENUS[-1]['_id'] + 1, "meal_name": meal_name, "meal_id": meal_id })
    #     return MOCK_MENUS
