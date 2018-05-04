"""unittests for orders in bookameal"""

import unittest
import json
import base64

from api import app

class TestMeals(unittest.TestCase):
    def setUp(self):
        """Method which i run before every test"""
        self.client = app.test_client(self)

    def tearDown(self):
        """Called after each test method."""
        pass

    def test_new_order(self):
        response = self.client.post('/api/v1/orders/1')
        self.assertIn(b"Your order has been logged and a you will be served shortly",
                     response.data)

    def test_new_order_with_inexistent_meal(self):
        response = self.client.post('/api/v1/orders/12')
        self.assertIn(b"Your order has been logged and a you will be served shortly", response.data)

    def test_get_all_orders(self):
        response = self.client.get('/api/v1/orders', headers={
                'Authorization': 'Basic ' + base64.b64encode(bytes('Ronald' + \
                ":" + 'Mutebi', 'ascii')).decode('ascii')
            })
        self.assertEqual(response.status_code, 200)

    def test_remove_order(self):
        response = self.client.delete('/api/v1/orders/1', headers={
                'Authorization': 'Basic ' + base64.b64encode(bytes('Ronald' + \
                ":" + 'Mutebi', 'ascii')).decode('ascii')
            })
        self.assertEqual(response.status_code, 202)

    def test_remove_order_with_non_existent_id(self):
        response = self.client.delete('/api/v1/orders/100', headers={
                'Authorization': 'Basic ' + base64.b64encode(bytes('Ronald' + \
                ":" + 'Mutebi', 'ascii')).decode('ascii')
            })
        self.assertEqual(response.status_code, 404)

if __name__ == "__main__":
    unittest.main()
    