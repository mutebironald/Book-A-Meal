"""unittests for orders in bookameal"""

import unittest
import json

from bookameal import app

class TestMeals(unittest.TestCase):
    def setUp(self):
        """Method which i run before every test"""
        self.client = app.test_client(self)

    def tearDown(self):
        """Called after each test method."""
        pass



# @app.route('/api/v1/orders')
# #@login_required
# @basic_auth.required
# def get_all_orders():
#     """Enables Authenticated caterer is able to get all orders""" 
#     now = datetime.datetime.utcnow()
#     orders = DB.get_orders(current_user.get_id())
#     for order in orders:
#         deltaseconds = (now - order['time']).seconds
#         order['wait_minutes'] = "{}.{}".format((deltaseconds/60),
#             str(deltaseconds % 60).zfill(2))
#     return jsonify({"orders": orders})


# #verify
# @app.route('/api/v1/orders/<order_id>')
# #@login_required
# def remove_order(order_id):
#     """Enables caterer to remove a particular order."""
#     order_id = request.args.get("order_id")
#     DB.delete_order(order_id)
#     return make_response("The order has been successfully removed", 202)

# @app.route('/api/v1/orders/<meal_id>', methods=['POST'])
# def new_order(meal_id):
#     """Enables customer to make an order"""
#     DB.add_order(meal_id, datetime.datetime.utcnow())
#     return "Your order has been logged and a you will be served shortly"

    # def test_get_menu(self):
    #     response = self.client.get('/api/v1/menu' )
    #     self.assertEqual(response.status_code, 200)
        

    # def test_setup_menu(self):
    #     response = self.client.post('/api/v1/menu', content_type = "application/json", data = json.dumps(dict(meal_name="cassava", meal_id=3)))
    #     self.assertEqual(response.status_code, 201)
        
    #not working
    def test_new_order(self):
        response = self.client.post('/api/v1/orders/2', content_type="application/json", data=json.dumps(dict(meal_id='2')))
        self.assertIn(b"Your order has been logged and a you will be served shortly", response.data)

if __name__ == "__main__":
    unittest.main()