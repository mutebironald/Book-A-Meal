"""unittests for menu in bookameal"""

import unittest
import json
import base64
from api import app


class TestMeals(unittest.TestCase):
    def setUp(self):
        """Method which i run before every test"""
        self.client = app.test_client(self)
        self.user = {
            "email": "rteroni@gmail.com",
            "password": "1234567"
        }
        self.meal = {
            "meal_name": "Katogo",
            "price": 4000
        }
        self.content = {
            "meal_id": "1"
        }

    def tearDown(self):
        """Called after each test method."""
        pass

    def test_get_menu(self):
        """Tests menu retrieval"""
        self.client.post('/api/v1/auth/signup',
                         content_type='application/json', data=json.dumps(self.user))
        response = self.client.post(
            '/api/v1/auth/login', content_type='application/json', data=json.dumps(self.user))
        data = json.loads(response.get_data())
        token = data['token']
        self.client.post('/api/v1/meals', data=json.dumps(self.meal),
                         content_type='application/json',  headers={'Authorization': token})
        self.client.get('/api/v1/meals', content_type='application/json',
                        headers={'Authorization': token})
        self.client.post('/api/v1/menu', content_type="application/json", data=json.dumps(self.content),  headers={
            'Authorization': token})
        response = self.client.get(
            '/api/v1/menu', headers={'Authorization': token})
        self.assertEqual(response.status_code, 200)

    def test_get_menu_without_token(self):
        """Test get menu without token."""
        self.client.post('/api/v1/auth/signup',
                         content_type='application/json', data=json.dumps(self.user))
        response = self.client.post(
            '/api/v1/auth/login', content_type='application/json', data=json.dumps(self.user))
        data = json.loads(response.data)
        token = data['token']
        self.client.post('/api/v1/meals', data=json.dumps(self.meal),
                         content_type='application/json',  headers={'Authorization': token})
        self.client.get('/api/v1/meals', content_type='application/json',
                        headers={'Authorization': token})
        self.client.post('/api/v1/menu', content_type="application/json", data=json.dumps(self.content),  headers={
            'Authorization': token})
        response = self.client.get('/api/v1/menu')
        self.assertEqual(response.status_code, 400)

    def test_get_menu_without_signup(self):
        """Test get menu without registration"""
        self.client.post('/api/v1/meals', data=json.dumps(self.meal),
                         content_type='application/json')
        self.client.get('/api/v1/meals', content_type='application/json')
        self.client.post(
            '/api/v1/menu', content_type="application/json", data=json.dumps(self.content))
        response = self.client.get('/api/v1/menu')
        self.assertEqual(response.status_code, 400)

    def test_setup_menu(self):
        """"Test menu creation"""
        self.client.post('/api/v1/auth/signup',
                         content_type='application/json', data=json.dumps(self.user))
        response = self.client.post(
            '/api/v1/auth/login', content_type='application/json', data=json.dumps(self.user))
        data = json.loads(response.data)
        token = data['token']
        self.client.post('/api/v1/meals', data=json.dumps(self.meal),
                         content_type='application/json',  headers={'Authorization': token})
        response = self.client.post('/api/v1/menu', content_type="application/json", data=json.dumps(self.content),  headers={
            'Authorization': token})
        self.assertEqual(response.status_code, 201)


if __name__ == "__main__":
    unittest.main()
