"""unittests for menu in bookameal"""

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

    def test_get_menu(self):
        user = {
            "email": "rteroni@gmail.com",
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
        data = json.loads(response.data)
        token = data['token']
        response = self.client.post('/api/v1/meals', data=json.dumps(meal), content_type='application/json',  headers={'Authorization': token})
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/api/v1/meals', content_type='application/json', headers={'Authorization': token})
        self.assertEqual(response.status_code, 200)
        response = self.client.post('/api/v1/menu', content_type = "application/json", data=json.dumps(content),  headers={
                'Authorization': token})
        self.assertEqual(response.status_code, 201)
        response = self.client.get('/api/v1/menu' , headers={'Authorization': token})
        self.assertEqual(response.status_code, 200)

    def test_get_menu_without_token(self):
        user = {
            "email": "barcaroni@gmail.com",
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
        data = json.loads(response.data)
        token = data['token']
        response = self.client.post('/api/v1/meals', data=json.dumps(meal), content_type='application/json',  headers={'Authorization': token})
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/api/v1/meals', content_type='application/json', headers={'Authorization': token})
        self.assertEqual(response.status_code, 200)
        response = self.client.post('/api/v1/menu', content_type = "application/json", data=json.dumps(content),  headers={
                'Authorization': token})
        self.assertEqual(response.status_code, 201)
        response = self.client.get('/api/v1/menu')
        self.assertEqual(response.status_code, 500)

    def test_get_menu_without_signup(self):
        content = {
            'meal_id':'2'
        }
        meal = {
            'meal_name':'Katogo',
            'price': 4000
        }
        response = self.client.post('/api/v1/meals', data=json.dumps(meal), content_type='application/json')
        response = self.client.get('/api/v1/meals', content_type='application/json')
        response = self.client.post('/api/v1/menu', content_type = "application/json", data=json.dumps(content))
        response = self.client.get('/api/v1/menu')
        self.assertEqual(response.status_code, 500)
        
    def test_setup_menu(self):
        meal = {
            'meal_name':'Katogo',
            'price': 4000
        }
        content = {
            'meal_id':'2'
        }
        user = {
            "email": "mroni@gmail.com",
            "password": "1234567"
        }
        signup = self.client.post('/api/v1/auth/signup', content_type='application/json', data=json.dumps(user) )
        self.assertEqual(signup.status_code, 201)
        response = self.client.post('/api/v1/auth/login', content_type='application/json', data = json.dumps(user))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        token = data['token']
        response = self.client.post('/api/v1/meals', data=json.dumps(meal), content_type='application/json',  headers={'Authorization': token})
        self.assertEqual(response.status_code, 200)
        response = self.client.post('/api/v1/menu', content_type = "application/json", data=json.dumps(content),  headers={
                'Authorization': token})
        self.assertEqual(response.status_code, 201)
        
if __name__ == "__main__":
    unittest.main()
