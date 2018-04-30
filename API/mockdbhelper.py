import datetime


#MOCK_USERS = {'ronald@gmail.com' : '123456'}

MOCK_USERS = [
    {"email": "ronald@example.com",
     "salt": "8Fb23mMNHD5Zb8pr2qWA3PE9bH0=",
     "hashed": "1736f83698df3f8153c1fbd6ce2840f8aace4f200771a46672635374073cc876cf0aa6a31f780e576578f791b5555b50df46303f0c3a7f2d21f91aa1429ac22e"}]

MOCK_MEALS = [{
    '_id': '1',
     'mealname': 'Beef with Rice',
     'owner':'ronald@example.com'}]

MOCK_ORDERS = [{
    "_id": "1",
     "meal_name": "Beef with Rice", 
     "meal_id": "1", 
     "time": datetime.datetime.utcnow()}]

class MockDBHelper:

    def get_user(self, email):
        user = [x for x in MOCK_USERS if x.get("email") == email]
        if user:
            return user[0]
        return None

    def add_user(self, email, salt, hashed):
        MOCK_USERS.append({"email" : email, "salt": salt, "hashed":hashed})


    def add_meal(self, mealname, owner):
        MOCK_MEALS.append({'_id': MOCK_MEALS[-1]['_id'] + 1 , 'mealname': mealname, 'owner': owner})
        return mealname

    def update_meal(self, _id, mealname):
        for meal in MOCK_MEALS:
            if meal.get('_id') == _id:
                meal['mealname'] = mealname
                break


    #Implementing for only one user
    def get_meals(self, owner_id):
        return MOCK_MEALS
        #for meal in MOCK_MEALS:
            #if meal.get("owner_id") == owner_id:
                #return MOCK_MEALS

    def get_meal(self, meal_id):
        for meal in MOCK_MEALS:
            if meal.get("_id") == meal_id:
                return meal

    def delete_meal(self, meal_id):
        for i, meal in enumerate(MOCK_MEALS):
            if meal.get("_id") == meal_id:
                del MOCK_MEALS[i]
            break

    def add_order(self, meal_id, time):
        meal = self.get_meal(meal_id)
        MOCK_ORDERS.append({'_id':meal_id, "owner": meal["owner"], "meal_name": meal["mealname"], "meal_id": meal_id, "time": time})
        return True
        


    def get_orders(self, owner_id):
        return MOCK_ORDERS

    def delete_order(self, order_id):
        for i, order in enumerate(MOCK_ORDERS):
            if order.get("_id") == order_id:
                del MOCK_ORDERS[i]
                break
        

