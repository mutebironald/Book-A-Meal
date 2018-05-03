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

    def test_new_order(self):
        response = self.client.post('/api/v1/orders/1')
        self.assertIn(b"Your order has been logged and a you will be served shortly", response.data)

    def test_get_all_orders(self):
        response = self.client.get('/api/v1/orders')
        self.assertEqual(response.status_code, 200)

    def test_remove_order(self):
        response = self.client.delete('/api/v1/orders/1')
        self.assertEqual(response.status_code, 202)

    def test_remove_order_with_non_existent_id(self):
        response = self.client.delete('/api/v1/orders/100')
        self.assertEqual(response.status_code, 404)

    



# #verify
# @app.route('/api/v1/orders/<meal_id>', methods=['POST'])
# def new_order(meal_id):
#     """Enables customer to make an order"""
#     DB.add_order(meal_id, datetime.datetime.utcnow())
#     return "Your order has been logged and a you will be served shortly"



# @app.route('/api/v1/orders')
# #@basic_auth.required
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
# #@basic_auth.required
# def remove_order(order_id):
#     """Enables caterer to remove a particular order."""
#     order_id = request.args.get("order_id")
#     DB.delete_order(order_id)
#     return make_response("The order has been successfully removed", 202)
        

if __name__ == "__main__":
    unittest.main()