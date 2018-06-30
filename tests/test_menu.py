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
        """Tests menu retrieval"""
        user = {
            "email": "rteroni@gmail.com",
            "password": "1234567"
        }
        content = {
            "meal_id":"2"
        }
        meal = {
            "meal_name":"Katogo",
            "price": 4000
        }
        self.client.post('/api/v1/auth/signup', content_type='application/json', data=json.dumps(user) )
        response = self.client.post('/api/v1/auth/login', content_type='application/json', data = json.dumps(user))
        data = json.loads(response.data)
        token = data['token']
        self.client.post('/api/v1/meals', data=json.dumps(meal), content_type='application/json',  headers={'Authorization': token})
        self.client.get('/api/v1/meals', content_type='application/json', headers={'Authorization': token})
        self.client.post('/api/v1/menu', content_type = "application/json", data=json.dumps(content),  headers={
                'Authorization': token})
        response = self.client.get('/api/v1/menu' , headers={'Authorization': token})
        self.assertEqual(response.status_code, 200)

    def test_get_menu_without_token(self):
        """Test get menu without token."""
        user = {
            "email": "barcaroni@gmail.com",
            "password": "1234567"
        }
        content = {
            "meal_id":"2"
        }
        meal = {
            "meal_name":"Katogo",
            "price": 4000
        }
        self.client.post('/api/v1/auth/signup', content_type='application/json', data=json.dumps(user) )
        response = self.client.post('/api/v1/auth/login', content_type='application/json', data = json.dumps(user))
        data = json.loads(response.data)
        token = data['token']
        self.client.post('/api/v1/meals', data=json.dumps(meal), content_type='application/json',  headers={'Authorization': token})
        self.client.get('/api/v1/meals', content_type='application/json', headers={'Authorization': token})
        self.client.post('/api/v1/menu', content_type = "application/json", data=json.dumps(content),  headers={
                'Authorization': token})
        response = self.client.get('/api/v1/menu')
        self.assertEqual(response.status_code, 500)

    def test_get_menu_without_signup(self):
        """Test get menu without registration"""
        content = {
            "meal_id":"2"
        }
        meal = {
            "meal_name":"Katogo",
            "price": 4000
        }
        self.client.post('/api/v1/meals', data=json.dumps(meal), content_type='application/json')
        self.client.get('/api/v1/meals', content_type='application/json')
        self.client.post('/api/v1/menu', content_type = "application/json", data=json.dumps(content))
        response = self.client.get('/api/v1/menu')
        self.assertEqual(response.status_code, 500)
        
    def test_setup_menu(self):
        """"Test menu creation"""
        meal = {
            "meal_name":"Katogo",
            "price": 4000
        }
        content = {
            "meal_id":"2"
        }
        user = {
            "email": "mroni@gmail.com",
            "password": "1234567"
        }
        self.client.post('/api/v1/auth/signup', content_type='application/json', data=json.dumps(user))
        response = self.client.post('/api/v1/auth/login', content_type='application/json', data = json.dumps(user))
        data = json.loads(response.data)
        token = data['token']
        self.client.post('/api/v1/meals', data=json.dumps(meal), content_type='application/json',  headers={'Authorization': token})
        response = self.client.post('/api/v1/menu', content_type = "application/json", data=json.dumps(content),  headers={
                'Authorization': token})
        self.assertEqual(response.status_code, 201)
        
if __name__ == "__main__":
    unittest.main()
