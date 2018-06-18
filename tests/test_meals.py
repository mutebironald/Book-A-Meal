"""unittests for meals in bookameal"""

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

    def test_get_meal(self):
        user = {
            "email": "roni@gmail.com",
            "password": "1234567"
        }
        signup = self.client.post('/api/v1/auth/signup', content_type='application/json', data=json.dumps(user) )
        self.assertEqual(signup.status_code, 201)
        response = self.client.post('/api/v1/auth/login', content_type='application/json', data = json.dumps(user))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        token = data['token']
        response = self.client.get('/api/v1/meals', content_type='application/json', headers={'Authorization': token})
        print(token)
        self.assertEqual(response.status_code, 200)

    def test_account_create_meal(self):
        content = {
            'meal_name':'Katogo',
            'price': 4000
        }
        user = {
            "email": "rrroni@gmail.com",
            "password": "1234567"
        }
        signup = self.client.post('/api/v1/auth/signup', content_type='application/json', data=json.dumps(user) )
        self.assertEqual(signup.status_code, 201)
        response = self.client.post('/api/v1/auth/login', content_type='application/json', data = json.dumps(user))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data())
        token = data['token']
        response = self.client.post('/api/v1/meals', data=json.dumps(content), content_type='application/json',  headers={'Authorization': token})
        self.assertEqual(response.status_code, 200)

    def test_account_create_meal_without_mealname(self):
        content = {
            'meal_name':'',
            'price':'3000'
        }
        user = {
            "email": "erroni@gmail.com",
            "password": "1234567"
        }
        signup = self.client.post('/api/v1/auth/signup', content_type='application/json', data=json.dumps(user) )
        self.assertEqual(signup.status_code, 201)
        response = self.client.post('/api/v1/auth/login', content_type='application/json', data = json.dumps(user))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data())
        token = data['token']
        response = self.client.post('/api/v1/meals', data=json.dumps(content), content_type='application/json', headers={
                'Authorization': token})
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Please enter a meal_name and price", response.data)

    def test_account_create_meal_without_name(self):
        content = {
            'meal_name':'',
            'price':'3000',
        }
        user = {
            "email": "zezrroni@gmail.com",
            "password": "1234567"
        }
        signup = self.client.post('/api/v1/auth/signup', content_type='application/json', data=json.dumps(user) )
        self.assertEqual(signup.status_code, 201)
        response = self.client.post('/api/v1/auth/login', content_type='application/json', data = json.dumps(user))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data())
        token = data['token']
       
        response = self.client.post('/api/v1/meals', data=json.dumps(content), content_type='application/json', headers={
                'Authorization': token})
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Please enter a meal_name and price", response.data)
 
    def test_account_update_meal(self):
        content = {
            'meal_name': 'Rice with gnuts',
            'price': 2000
        }
        user = {
            "email": "sagrt@gmail.com",
            "password": "1234567"
        }
        signup = self.client.post('/api/v1/auth/signup', content_type='application/json', data=json.dumps(user) )
        self.assertEqual(signup.status_code, 201)
        response = self.client.post('/api/v1/auth/login', content_type='application/json', data = json.dumps(user))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data())
        token = data['token']

        response = self.client.put('/api/v1/meals/1', data=json.dumps(content), content_type='application/json', headers={
                'Authorization': token}) 
        self.assertEqual(response.status_code, 200)

    def test_account_update_meal_without_data(self):
        
        content = {
            'meal_name': '',
            'price': 2000
        }
        user = {
            "email": "sgrt@gmail.com",
            "password": "1234567"
        }
        signup = self.client.post('/api/v1/auth/signup', content_type='application/json', data=json.dumps(user) )
        self.assertEqual(signup.status_code, 201)
        response = self.client.post('/api/v1/auth/login', content_type='application/json', data = json.dumps(user))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data())
        token = data['token']

        response = self.client.put('/api/v1/meals/2', data=json.dumps(content), content_type='application/json',  headers={
                'Authorization': token})
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Please enter a meal name", response.data)

    def test_account_delete_meal(self):
        user = {
            "email": "herart@gmail.com",
            "password": "1234567"
        }
        content = {
            'meal_name':'Katogo',
            'price': 4000
        }
        signup = self.client.post('/api/v1/auth/signup', content_type='application/json', data=json.dumps(user) )
        self.assertEqual(signup.status_code, 201)
        response = self.client.post('/api/v1/auth/login', content_type='application/json', data = json.dumps(user))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data())
        token = data['token']
        response = self.client.post('/api/v1/meals', data=json.dumps(content), content_type='application/json',  headers={'Authorization': token})
        self.assertEqual(response.status_code, 200)
        response = self.client.delete('/api/v1/meals/1',headers={'Authorization': token} )
        self.assertEqual(response.status_code, 202)
        self.assertIn(b"The meal has been deleted", response.data)

if __name__ == "__main__":
    unittest.main()
    