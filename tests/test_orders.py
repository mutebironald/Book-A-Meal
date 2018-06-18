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
        order = {
            "meal_id": "2"
        }
        user = {
            "email": "ytroni@gmail.com",
            "password": "1234567"
        }
        content = {
            'meal_id':'2'
        }
        meal = {
            'meal_name':'Katogo',
            'price': 4000
        }
        signup = self.client.post('/api/v1/auth/signup', content_type='application/json', data=json.dumps(user) )
        self.assertEqual(signup.status_code, 201)
        response = self.client.post('/api/v1/auth/login', content_type='application/json', data = json.dumps(user))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data())
        token = data['token']
        response = self.client.post('/api/v1/meals', data=json.dumps(meal), content_type='application/json',  headers={'Authorization': token})
        self.assertEqual(response.status_code, 200)
        response = self.client.post('/api/v1/menu', content_type = "application/json", data=json.dumps(content),  headers={
                'Authorization': token})
        self.assertEqual(response.status_code, 201)
        response = self.client.post('/api/v1/orders', data=json.dumps(order),content_type = 'application/json', headers={
                'Authorization': token})
        self.assertIn(b"Your order has been logged and a you will be served shortly", response.data)
        
    def test_get_all_orders(self):
        order = {
            "meal_id": "2"
        }
        user = {
            "email": "groni@gmail.com",
            "password": "1234567"
        }
        content = {
            'meal_id':'2'
        }
        meal = {
            'meal_name':'Katogo',
            'price': 4000
        }
        signup = self.client.post('/api/v1/auth/signup', content_type='application/json', data=json.dumps(user) )
        self.assertEqual(signup.status_code, 201)
        response = self.client.post('/api/v1/auth/login', content_type='application/json', data = json.dumps(user))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data())
        token = data['token']
        response = self.client.post('/api/v1/meals', data=json.dumps(meal), content_type='application/json',  headers={'Authorization': token})
        self.assertEqual(response.status_code, 200)
        response = self.client.post('/api/v1/menu', content_type = "application/json", data=json.dumps(content),  headers={
                'Authorization': token})
        self.assertEqual(response.status_code, 201)
        response = self.client.post('/api/v1/orders', data=json.dumps(order),content_type = 'application/json', headers={
                'Authorization': token})
        self.assertIn(b"Your order has been logged and a you will be served shortly", response.data)
        response = self.client.get('/api/v1/orders', headers={
                'Authorization': token})
        self.assertEqual(response.status_code, 200)

    def test_get_order(self):
        order = {
            "meal_id": "2"
        }
        user = {
            "email": "jejinga@gmail.com",
            "password": "1234567"
        }
        content = {
            'meal_id':'2'
        }
        meal = {
            'meal_name':'Katogo',
            'price': 4000
        }
        signup = self.client.post('/api/v1/auth/signup', content_type='application/json', data=json.dumps(user) )
        self.assertEqual(signup.status_code, 201)
        response = self.client.post('/api/v1/auth/login', content_type='application/json', data = json.dumps(user))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data())
        token = data['token']
        response = self.client.post('/api/v1/meals', data=json.dumps(meal), content_type='application/json',  headers={'Authorization': token})
        self.assertEqual(response.status_code, 200)
        response = self.client.post('/api/v1/menu', content_type = "application/json", data=json.dumps(content),  headers={
                'Authorization': token})
        self.assertEqual(response.status_code, 201)
        response = self.client.post('/api/v1/orders', data=json.dumps(order),content_type = 'application/json', headers={
                'Authorization': token})
        self.assertIn(b"Your order has been logged and a you will be served shortly", response.data)
        response = self.client.get('/api/v1/orders/1', headers={
                'Authorization': token
            })
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()
    