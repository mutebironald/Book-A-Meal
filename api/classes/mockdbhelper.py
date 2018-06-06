import datetime

MOCK_USERS = [
    {
    "email": "ronald@gmail.com",
    "role": "Admin",
    "salt": "8Fb23mMNHD5Zb8pr2qWA3PE9bH0=",
    "hashed": "1736f83698df3f8153c1fbd6ce2840f8aace4f200771a46672635374073cc876cf0aa6a31f780e576578f791b5555b50df46303f0c3a7f2d21f91aa1429ac22e"
     }]

MOCK_MEALS = [{
    '_id': 1,
    'meal_name': 'Beef with Rice',
    'price': 3000,
    'owner':'ronald@gmail.com'
    }]

MOCK_ORDERS = [{
    "_id": 1,
    "meal_name": "Beef with Rice", 
    "meal_id": "1", 
    "time": datetime.datetime.utcnow()
    }]

new_menu =[
    {
        'id': 1,
        'day': 'monday',
        'meal':{
            'id': 3,
            'name': 'matooke',
            'price': 'UGX 15,000'
        }
        
    }
]


class MockDBHelper:
    """
    This class handles all methods associated
    with the user, meals, menu and order.
    """

    def get_user(self, email):
        """Helps am already registered user to log in."""
        available_user = [user for user in MOCK_USERS if user["email"] == email]
        print(available_user)
        if available_user:
            return available_user[0]
        return None

    def add_user(self, email, salt, hashed):
        """Enables user registration or signup"""
        MOCK_USERS.append({
            "email" : email, 
            "salt": salt,
            "hashed":hashed
            })

    def add_meal(self, meal_name, price,  owner):
        """Enables caterer to add a meal option"""
        MOCK_MEALS.append({
            '_id': MOCK_MEALS[-1]['_id'] + 1 ,
            'meal_name': meal_name,
            'price': price
            })

        return meal_name

    def update_meal(self, _id, meal_name, price):
        """Enables caterer to change a specific meal option"""
        for meal in MOCK_MEALS:
            if u"{}".format(meal.get('_id')) == _id:
                meal['meal_name'] = meal_name
                meal['price'] = price
                break
           
    def get_meals(self, owner_id):
        """Returns all available meal options"""
        for meal in MOCK_MEALS:
            if meal.get("owner_id") == owner_id:
                return MOCK_MEALS
            break

    def get_meal(self, meal_id):
        """To get meals from meal options"""
        for meal in MOCK_MEALS:
            if u"{}".format(meal.get('_id')) == meal_id:
                return meal

    def delete_meal( self, meal_id):
        """Enables the caterer to resolve/remove orders"""
        meal = [(i, meal) for i, meal in enumerate(MOCK_MEALS) if meal['_id'] == meal_id]
        if meal:
            print(MOCK_MEALS[meal[0][0]])
            MOCK_MEALS.remove(MOCK_MEALS[meal[0][0]])
            print(meal)
            return True
        else:
            return False

    def add_order(self, meal_id, time):
        """Enables customer to make an order."""
        meal = self.get_menu(meal_id)
        if meal:
            MOCK_ORDERS.append({
                '_id':MOCK_ORDERS[-1]['_id'] + 1, 
                "meal_name": meal["meal_name"], 
                "meal_id": meal_id, 
                "time": time
                })
            return True
        else:
            return False
    
    def get_orders(self, owner_id):
        """Returns all orders belonging to a particular caterer"""
        return MOCK_ORDERS

    def delete_order( self, order_id):
        """Enables the caterer to resolve/remove orders"""
        order = [(i, order) for i, order in enumerate(MOCK_ORDERS) if order['_id'] == order_id]
        if order:
            MOCK_ORDERS.remove(MOCK_ORDERS[order[0][0]])
            return True
        return False
        
    def get_menu(self, day):
        for menu in new_menu:
            if menu['day'] == day:
                return menu

    def setup_menu(self, meal_name, day, price):
        new_menu.append(
            {
                'day': day,
                'meal': {
                    'name': meal_name,
                    'price': price
                }
            }
        )
        return new_menu

    # def setup_menu(self, meal_id, meal_name):
    #     """Enables caterer to setup menu for the day"""
    #     MOCK_MENUS.append({"_id": MOCK_MENUS[-1]['_id'] + 1, "meal_name": meal_name, "meal_id": meal_id })
    #     return MOCK_MENUS
