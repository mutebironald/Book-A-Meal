class User():

    USERS = [{'id':1, 'email':'ronald@gmail.com', 'password':'123456', 'authenticated':False},
            {'id':2, 'email':'mutebi@gmail.com', 'password':'123hdg', 'authenticated':True}]

    def login_user(self, email, password):
        """This represents a sign/login in"""
        user = [x for x in USERS if x.get('email') ==email if x.get('password')==password]

        if user:
            return user[0]
        return None

    def register_user(self, email, password,passord2):
        """This represents a user registration"""
        for x in self.USERS:
            if x.get('email') == email:
                return "You are already registered"
            else:
                if password == password2:
                    user = {'email': email, 'password':password}
                    self.USERS.append(user)
                    return "You have registered successfully"





class Order():

    ORDERS = [{'order_id':3, 'user_id':'id', 'meal':'meal_name'}]

    def get_orders(self):
        all_orders = [ d for d in ORDERS ]
        return all_orders

    def get_specific order('order_id'):
        specific_order = [ k for k in ORDERS if order_id =ORDERS['order_id'] ]
        return specific_order


class Menu():
    MENUS = [{'day': 'Monday', 'menu':[{'meal_name':'Kikomando', 'price':1700, 'user_id':'id'},
    {'meal_name':'Posho and chicken', 'price':3400, 'user_id':'id'}] }]

    def save(self, day, menu):
        self.menus.append( { 'day': day, 'menu':menu } )

    def edit_menu(self, day, menu):
        if menu in MENUS['menu']:


class Meal():

    MEALS =[{'meal_name':'Kikomando', 'price':1700, 'user_id':'id'},
        {'meal_name':'Posho and chicken', 'price':3400, 'user_id':'id'}]


    meal = [{'meal_name':'Beef with rice', 'price':3000}, {'meal_name':'Minced goat meet', 'price':7000}]
    def save_meal(self, meal):
        for x in MEALS:
            if x['meal_name'] ==meal['meal_name']:
                return "The meal is already Present"
            else:
                MEALS.append(meal)
            return "The meal is now in the menu"

        

    def get_all_meals(self):
        return self.MEALS

            





