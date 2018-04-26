import unittest
import json

from app import app

class TestOrder(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client(self)

    def test_ability_to_make_order(self):
        """Tests that a customer/client is able to make an order"""
        self.client.post('/api/v1/meals/', content_type='application/json', data=json.dumps(dict(meal_name='Pilao and greens', price=2000)))
        self.client.post('/api/v1/meals/', content_type='application/json',data=json.dumps(dict(meal_name='Chaps na chapati', price=1000)))
        self.client.post('/api/v1/meals/', content_type='application/json', data=json.dumps(dict(meal_name='Cassava and Gnuts', price=7000)))

        self.client.post('/api/v1/menu/3')
        self.client.post('/api/v1/menu/5')
        response = self.client.post('/api/v1/orders/3')
        self.assertIn(u'Successfully sent', response.data)

if __name__ == '__main__':
    unittest.main()