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
        """Test wether API can get all meals"""
        user = {
            "email": "roni@gmail.com",
            "password": "1234567"
        }
        self.client.post('/api/v1/auth/signup', content_type='application/json', data=json.dumps(user) )
        response = self.client.post('/api/v1/auth/login', content_type='application/json', data = json.dumps(user))
        data = json.loads(response.data)
        token = data['token']
        response = self.client.get('/api/v1/meals', content_type='application/json', headers={'Authorization': token})
        self.assertEqual(response.status_code, 200)

    def test_get_meal_without_token(self):
        """Tests get meal without token"""
        user = {
            "email": "cfconi@gmail.com",
            "password": "1234567"
        }
        self.client.post('/api/v1/auth/signup', content_type='application/json', data=json.dumps(user) )
        response = self.client.post('/api/v1/auth/login', content_type='application/json', data = json.dumps(user))
        data = json.loads(response.data)
        token = data['token']
        response = self.client.get('/api/v1/meals', content_type='application/json')
        self.assertEqual(response.status_code, 500)

    def test_get_meal_without_registration(self):
        """tests wether an anonymous user can get meals"""
        response = self.client.get('/api/v1/meals', content_type='application/json')
        self.assertEqual(response.status_code, 500)

    def test_account_create_meal(self):
        """Tests meal creation"""
        content = {
            "meal_name":"Katogo",
            "price": 4000
        }
        user = {
            "email": "rrroni@gmail.com",
            "password": "1234567"
        }
        self.client.post('/api/v1/auth/signup', content_type='application/json', data=json.dumps(user) )
        response = self.client.post('/api/v1/auth/login', content_type='application/json', data = json.dumps(user))
        data = json.loads(response.get_data())
        token = data['token']
        response = self.client.post('/api/v1/meals', data=json.dumps(content), content_type='application/json',  headers={'Authorization': token})
        self.assertEqual(response.status_code, 200)

    def test_account_create_meal_without_mealname(self):
        """tests meal creation without meal name"""
        content = {
            "meal_name":"",
            "price":3000
        }
        user = {
            "email": "erroni@gmail.com",
            "password": "1234567"
        }
        self.client.post('/api/v1/auth/signup', content_type='application/json', data=json.dumps(user) )
        response = self.client.post('/api/v1/auth/login', content_type='application/json', data = json.dumps(user))
        data = json.loads(response.get_data())
        token = data['token']
        response = self.client.post('/api/v1/meals', data=json.dumps(content), content_type='application/json', headers={
                'Authorization': token})
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Enter a valid meal name and price", response.data)

    def test_account_create_meal_without_price(self):
        """Tests meal creation without price"""
        content = {
            "meal_name":"resty",
            "price":"",
        }
        user = {
            "email": "zezrroni@gmail.com",
            "password": "1234567"
        }
        self.client.post('/api/v1/auth/signup', content_type='application/json', data=json.dumps(user) )
        response = self.client.post('/api/v1/auth/login', content_type='application/json', data = json.dumps(user))
        data = json.loads(response.get_data())
        token = data['token']
        response = self.client.post('/api/v1/meals', data=json.dumps(content), content_type='application/json', headers={
                'Authorization': token})
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Enter a valid meal name and price", response.data)

    def test_account_create_meal_without_data(self):
        """Tests meal creation without meal name and price"""
        content = {
            "meal_name":"",
            "price":"",
        }
        user = {
            "email": "gerrroni@gmail.com",
            "password": "1234567"
        }
        self.client.post('/api/v1/auth/signup', content_type='application/json', data=json.dumps(user) )
        response = self.client.post('/api/v1/auth/login', content_type='application/json', data = json.dumps(user))
        data = json.loads(response.get_data())
        token = data['token']
        response = self.client.post('/api/v1/meals', data=json.dumps(content), content_type='application/json', headers={
                'Authorization': token})
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Enter a valid meal name and price", response.data)

    def test_account_create_meal_without_token(self):
        """Tests meal creation without Token"""
        content = {
            "meal_name":"Katogo",
            "price": 4000
        }
        user = {
            "email": "himroni@gmail.com",
            "password": "1234567"
        }
        self.client.post('/api/v1/auth/signup', content_type='application/json', data=json.dumps(user) )
        response = self.client.post('/api/v1/auth/login', content_type='application/json', data = json.dumps(user))
        data = json.loads(response.get_data())
        token = data['token']
        response = self.client.post('/api/v1/meals', data=json.dumps(content), content_type='application/json')
        self.assertEqual(response.status_code, 500)
 
    def test_account_update_meal(self):
        """Tests meal update"""
        content = {
            "meal_name": "Rice with gnuts",
            "price": 2000
        }
        user = {
            "email": "sagrt@gmail.com",
            "password": "1234567"
        }
        self.client.post('/api/v1/auth/signup', content_type='application/json', data=json.dumps(user) )
        response = self.client.post('/api/v1/auth/login', content_type='application/json', data = json.dumps(user))
        data = json.loads(response.get_data())
        token = data['token']
        response = self.client.put('/api/v1/meals/1', data=json.dumps(content), content_type='application/json', headers={
                'Authorization': token}) 
        self.assertEqual(response.status_code, 200)

    def test_account_update_meal_without_mealname(self):
        """Tests meal update without meal name"""
 
        content = {
            "meal_name": "",
            "price": 2000
        }
        user = {
            "email": "sgrt@gmail.com",
            "password": "1234567"
        }
        self.client.post('/api/v1/auth/signup', content_type='application/json', data=json.dumps(user) )
        response = self.client.post('/api/v1/auth/login', content_type='application/json', data = json.dumps(user))
        data = json.loads(response.get_data())
        token = data['token']
        response = self.client.put('/api/v1/meals/2', data=json.dumps(content), content_type='application/json',  headers={
                'Authorization': token})
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Enter a valid meal name and price", response.data)

    def test_account_update_meal_without_price(self):
        """Tests meal update without price"""
        
        content = {
            "meal_name": "kikajjo",
            "price": ""
        }
        user = {
            "email": "sgxxsßrt@gmail.com",
            "password": "1234567"
        }
        self.client.post('/api/v1/auth/signup', content_type='application/json', data=json.dumps(user) )
        response = self.client.post('/api/v1/auth/login', content_type='application/json', data = json.dumps(user))
        data = json.loads(response.get_data())
        token = data['token']
        response = self.client.put('/api/v1/meals/2', data=json.dumps(content), content_type='application/json',  headers={
                'Authorization': token})
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Enter a valid meal name and price", response.data)

    def test_account_update_meal_without_data(self):
        """Tests meal update without meal name and price"""
        
        content = {
            "meal_name": "",
            "price": ""
        }
        user = {
            "email": "moirt@gmail.com",
            "password": "1234567"
        }
        self.client.post('/api/v1/auth/signup', content_type='application/json', data=json.dumps(user) )
        response = self.client.post('/api/v1/auth/login', content_type='application/json', data = json.dumps(user))
        data = json.loads(response.get_data())
        token = data['token']
        response = self.client.put('/api/v1/meals/2', data=json.dumps(content), content_type='application/json',  headers={
                'Authorization': token})
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Enter a valid meal name and price", response.data)

    def test_account_update_meal_without_token(self):
        """Tests meal update without token"""
        content = {
            "meal_name": "Rice with gnuts",
            "price": 2000
        }
        user = {
            "email": "cnnrt@gmail.com",
            "password": "1234567"
        }
        self.client.post('/api/v1/auth/signup', content_type='application/json', data=json.dumps(user) )
        response = self.client.post('/api/v1/auth/login', content_type='application/json', data = json.dumps(user))
        data = json.loads(response.get_data())
        token = data['token']
        response = self.client.put('/api/v1/meals/1', data=json.dumps(content), content_type='application/json') 
        self.assertEqual(response.status_code, 500)

    def test_account_delete_meal(self):
        """tests meal deletion"""
        user = {
            "email": "herart@gmail.com",
            "password": "1234567"
        }
        content = {
            "meal_name":"Katogo",
            "price": 4000
        }
        self.client.post('/api/v1/auth/signup', content_type='application/json', data=json.dumps(user) )
        response = self.client.post('/api/v1/auth/login', content_type='application/json', data = json.dumps(user))
        data = json.loads(response.get_data())
        token = data['token']
        self.client.post('/api/v1/meals', data=json.dumps(content), content_type='application/json',  headers={'Authorization': token})
        response = self.client.delete('/api/v1/meals/1',headers={'Authorization': token} )
        self.assertEqual(response.status_code, 202)
        self.assertIn(b"The meal has been deleted", response.data)

    def test_account_delete_meal_twice(self):
        """"Tests double meal deletion"""
        user = {
            "email": "manuart@gmail.com",
            "password": "1234567"
        }
        content = {
            "meal_name":"kiKatogo",
            "price": 4000
        }
        self.client.post('/api/v1/auth/signup', content_type='application/json', data=json.dumps(user) )
        response = self.client.post('/api/v1/auth/login', content_type='application/json', data = json.dumps(user))
        data = json.loads(response.get_data())
        token = data['token']
        self.client.post('/api/v1/meals', data=json.dumps(content), content_type='application/json',  headers={'Authorization': token})
        self.client.delete('/api/v1/meals/1',headers={'Authorization': token} )
        response = self.client.delete('/api/v1/meals/1',headers={'Authorization': token} )
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"The meal specified is not present", response.data)

    def test_account_delete_nonexistent_meal(self):
        """Tests deletion of non existent meal"""
        user = {
            "email": "rherart@gmail.com",
            "password": "1234567"
        }
        content = {
            "meal_name":"Katogo",
            "price": 4000
        }
        self.client.post('/api/v1/auth/signup', content_type='application/json', data=json.dumps(user) )
        response = self.client.post('/api/v1/auth/login', content_type='application/json', data = json.dumps(user))
        data = json.loads(response.get_data())
        token = data['token']
        self.client.post('/api/v1/meals', data=json.dumps(content), content_type='application/json',  headers={'Authorization': token})
        response = self.client.delete('/api/v1/meals/54',headers={'Authorization': token} )
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"The meal specified is not present", response.data)

    def test_account_delete_meal_without_token(self):
        """Tests deletion of meal without token"""
        user = {
            "email": "csabaart@gmail.com",
            "password": "1234567"
        }
        content = {
            "meal_name":"Katogo",
            "price": 4000
        }
        self.client.post('/api/v1/auth/signup', content_type='application/json', data=json.dumps(user) )
        response = self.client.post('/api/v1/auth/login', content_type='application/json', data = json.dumps(user))
        data = json.loads(response.get_data())
        token = data['token']
        self.client.post('/api/v1/meals', data=json.dumps(content), content_type='application/json',  headers={'Authorization': token})
        response = self.client.delete('/api/v1/meals/1' )
        self.assertEqual(response.status_code, 500)
        

if __name__ == "__main__":
    unittest.main()
    