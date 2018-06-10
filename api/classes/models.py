import datetime

# meals = Meals()
# menu = Menu(meals)

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
            if meal['id'] == _id:
                meal['meal_name'] = meal_name
                meal['price'] = price
                break
    
    def get_meals(self):
        """Returns all available meal options"""
        return self.meals

    def get_meal(self, meal_id):
        """To get meals from meal options"""
        for meal in self.meals:
            if meal['id'] == meal_id:
                return meal
            

    def delete_meal( self, meal_id):
        """Enables the caterer to resolve/remove orders"""
        c = 0
        for meal in self.meals:
            if meal['id'] == meal_id:
                del self.meals[c]
                return True
            c += 1

class Menu:
    """A class to represent the Menu of meals for a particular day"""
    def __init__(self, meals):
        self.menu = []
        self.meals = meals

    def get_menu(self):
        return self.menu

    def setup_menu(self, meal_id):
        meal_get = self.meals.get_meals()
        for meal in meal_get:
            if meal['id'] == int(meal_id):
                print(meal)
                self.menu.append(meal)
                return self.menu
        return False

class Orders:
    """A class to represent a customers/users orders"""
    def __init__(self, menu):
        self.orders = []
        self.menu = menu
        self.id = 1

    def add_order(self, meal_id, time):
        """Enables customer to make an order."""
        menu_returned = self.menu.get_menu()
        for meal in menu_returned:
            if meal['id'] == int(meal_id):
                self.orders.append({
                    "id": self.id,
                    'meal': meal,
                    'time': time,
                    'cleared': False
                })
                self.id += 1
                print(self.id)
                return self.orders
            
    def get_orders(self):
        """Returns all orders belonging to a particular caterer"""
        return self.orders

    #getting an order
    def get_order(self, order_id):
        for order in self.orders:
            if order['id'] == order_id:
                return order

    def delete_order( self, order_id):
        """Enables the caterer to resolve/remove orders"""
        c = 0
        for order in self.orders:
            if order['id'] == order_id:
                del self.orders[c]
                return True
            c += 1
            
