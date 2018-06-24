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
        self.assertEqual(response.status_code, 200)

    def test_get_meal_without_token(self):
        user = {
            "email": "cfconi@gmail.com",
            "password": "1234567"
        }
        signup = self.client.post('/api/v1/auth/signup', content_type='application/json', data=json.dumps(user) )
        self.assertEqual(signup.status_code, 201)
        response = self.client.post('/api/v1/auth/login', content_type='application/json', data = json.dumps(user))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        token = data['token']
        response = self.client.get('/api/v1/meals', content_type='application/json')
        self.assertEqual(response.status_code, 500)

    def test_get_meal_without_registration(self):
        """tests wether an anonymous user can get meals"""
        response = self.client.get('/api/v1/meals', content_type='application/json')
        self.assertEqual(response.status_code, 500)

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
            'price':3000
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
        self.assertIn(b"Enter a valid meal name and price", response.data)

    def test_account_create_meal_without_price(self):
        content = {
            'meal_name':'resty',
            'price':'',
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
        self.assertIn(b"Enter a valid meal name and price", response.data)

    def test_account_create_meal_without_data(self):
        content = {
            'meal_name':'',
            'price':'',
        }
        user = {
            "email": "gerrroni@gmail.com",
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
        self.assertIn(b"Enter a valid meal name and price", response.data)

    def test_account_create_meal_without_token(self):
        content = {
            'meal_name':'Katogo',
            'price': 4000
        }
        user = {
            "email": "himroni@gmail.com",
            "password": "1234567"
        }
        signup = self.client.post('/api/v1/auth/signup', content_type='application/json', data=json.dumps(user) )
        self.assertEqual(signup.status_code, 201)
        response = self.client.post('/api/v1/auth/login', content_type='application/json', data = json.dumps(user))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data())
        token = data['token']
        response = self.client.post('/api/v1/meals', data=json.dumps(content), content_type='application/json')
        self.assertEqual(response.status_code, 500)
 
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

    def test_account_update_meal_without_mealname(self):
        
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
        self.assertIn(b"Enter a valid meal name and price", response.data)

    def test_account_update_meal_without_price(self):
        
        content = {
            'meal_name': 'kikajjo',
            'price': ""
        }
        user = {
            "email": "sgxxsßrt@gmail.com",
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
        self.assertIn(b"Enter a valid meal name and price", response.data)

    def test_account_update_meal_without_data(self):
        
        content = {
            'meal_name': '',
            'price': ""
        }
        user = {
            "email": "moirt@gmail.com",
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
        self.assertIn(b"Enter a valid meal name and price", response.data)

    def test_account_update_meal_without_token(self):
        content = {
            'meal_name': 'Rice with gnuts',
            'price': 2000
        }
        user = {
            "email": "cnnrt@gmail.com",
            "password": "1234567"
        }
        signup = self.client.post('/api/v1/auth/signup', content_type='application/json', data=json.dumps(user) )
        self.assertEqual(signup.status_code, 201)
        response = self.client.post('/api/v1/auth/login', content_type='application/json', data = json.dumps(user))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data())
        token = data['token']

        response = self.client.put('/api/v1/meals/1', data=json.dumps(content), content_type='application/json') 
        self.assertEqual(response.status_code, 500)

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

    def test_account_delete_meal_twice(self):
        user = {
            "email": "manuart@gmail.com",
            "password": "1234567"
        }
        content = {
            'meal_name':'kiKatogo',
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
        self.client.delete('/api/v1/meals/1',headers={'Authorization': token} )
        response = self.client.delete('/api/v1/meals/1',headers={'Authorization': token} )
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"The meal specified is not present", response.data)

    def test_account_delete_nonexistent_meal(self):
        user = {
            "email": "rherart@gmail.com",
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
        response = self.client.delete('/api/v1/meals/54',headers={'Authorization': token} )
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"The meal specified is not present", response.data)

    def test_account_delete_meal_without_token(self):
        user = {
            "email": "csabaart@gmail.com",
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
        response = self.client.delete('/api/v1/meals/1' )
        self.assertEqual(response.status_code, 500)
        

if __name__ == "__main__":
    unittest.main()
    