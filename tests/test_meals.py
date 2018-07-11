"""unittests for meals in bookameal"""

import unittest
import json
import base64

from api import app


class TestMeals(unittest.TestCase):
    def setUp(self):
        """Method which i run before every test"""
        self.client = app.test_client(self)
        self.user = {
            "email": "roni@gmail.com",
            "password": "1234567"
        }
        self.content = {
            "meal_name": "kikajjo",
            "price": ""
        }

    def tearDown(self):
        """Called after each test method."""
        pass

    def test_get_meal(self):
        """Test wether API can get all meals"""
        self.client.post('/api/v1/auth/signup',
                         content_type='application/json', data=json.dumps(self.user))
        response = self.client.post(
            '/api/v1/auth/login', content_type='application/json', data=json.dumps(self.user))
        data = json.loads(response.data.decode())
        token = data['token']
        response = self.client.get(
            '/api/v1/meals', content_type='application/json', headers={'Authorization': token})
        self.assertEqual(response.status_code, 200)

    def test_get_meal_without_token(self):
        """Tests get meal without token"""
        self.client.post('/api/v1/auth/signup',
                         content_type='application/json', data=json.dumps(self.user))
        response = self.client.post(
            '/api/v1/auth/login', content_type='application/json', data=json.dumps(self.user))
        data = json.loads(response.data)
        token = data['token']
        response = self.client.get(
            '/api/v1/meals', content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_get_meal_without_registration(self):
        """tests wether an anonymous user can get meals"""
        response = self.client.get(
            '/api/v1/meals', content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_account_create_meal(self):
        """Tests meal creation"""
        content = {
            "meal_name": "Katogo",
            "price": 4000
        }
        self.client.post('/api/v1/auth/signup',
                         content_type='application/json', data=json.dumps(self.user))
        response = self.client.post(
            '/api/v1/auth/login', content_type='application/json', data=json.dumps(self.user))
        data = json.loads(response.get_data())
        token = data['token']
        response = self.client.post('/api/v1/meals', data=json.dumps(
            content), content_type='application/json',  headers={'Authorization': token})
        self.assertEqual(response.status_code, 201)

    def test_account_create_meal_without_price(self):
        """Tests meal creation without price"""
        self.client.post('/api/v1/auth/signup',
                         content_type='application/json', data=json.dumps(self.user))
        response = self.client.post(
            '/api/v1/auth/login', content_type='application/json', data=json.dumps(self.user))
        data = json.loads(response.get_data())
        token = data['token']
        response = self.client.post('/api/v1/meals', data=json.dumps(self.content), content_type='application/json', headers={
            'Authorization': token})
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Enter a valid meal name and price", response.data)

    def test_account_create_meal_without_data(self):
        """Tests meal creation without meal name and price"""
        self.client.post('/api/v1/auth/signup',
                         content_type='application/json', data=json.dumps(self.user))
        response = self.client.post(
            '/api/v1/auth/login', content_type='application/json', data=json.dumps(self.user))
        data = json.loads(response.data.decode())
        token = data['token']
        response = self.client.post('/api/v1/meals', data=json.dumps(self.content), content_type='application/json', headers={
            'Authorization': token})
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Enter a valid meal name and price", response.data)

    def test_account_create_meal_without_token(self):
        """Tests meal creation without Token"""
        self.client.post('/api/v1/auth/signup',
                         content_type='application/json', data=json.dumps(self.user))
        response = self.client.post(
            '/api/v1/auth/login', content_type='application/json', data=json.dumps(self.user))
        data = json.loads(response.get_data())
        token = data['token']
        response = self.client.post(
            '/api/v1/meals', data=json.dumps(self.content), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_account_update_meal(self):
        """Tests meal update"""
        content = {
            "meal_name": "Rice with gnuts",
            "price": 2000
        }
        self.client.post('/api/v1/auth/signup',
                         content_type='application/json', data=json.dumps(self.user))
        response = self.client.post(
            '/api/v1/auth/login', content_type='application/json', data=json.dumps(self.user))
        data = json.loads(response.get_data())
        token = data['token']
        response = self.client.put('/api/v1/meals/1', data=json.dumps(content), content_type='application/json', headers={
            'Authorization': token})
        self.assertEqual(response.status_code, 200)

    def test_account_update_meal_without_mealname(self):
        """Tests meal update without meal name"""
        self.client.post('/api/v1/auth/signup',
                         content_type='application/json', data=json.dumps(self.user))
        response = self.client.post(
            '/api/v1/auth/login', content_type='application/json', data=json.dumps(self.user))
        data = json.loads(response.get_data())
        token = data['token']
        response = self.client.put('/api/v1/meals/2', data=json.dumps(self.content), content_type='application/json',  headers={
            'Authorization': token})
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Enter a valid meal name and price", response.data)

    def test_account_update_meal_without_price(self):
        """Tests meal update without price"""
        self.client.post('/api/v1/auth/signup',
                         content_type='application/json', data=json.dumps(self.user))
        response = self.client.post(
            '/api/v1/auth/login', content_type='application/json', data=json.dumps(self.user))
        data = json.loads(response.get_data())
        token = data['token']
        response = self.client.put('/api/v1/meals/2', data=json.dumps(self.content), content_type='application/json',  headers={
            'Authorization': token})
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Enter a valid meal name and price", response.data)

    def test_account_update_meal_without_data(self):
        """Tests meal update without meal name and price"""
        self.client.post('/api/v1/auth/signup',
                         content_type='application/json', data=json.dumps(self.user))
        response = self.client.post(
            '/api/v1/auth/login', content_type='application/json', data=json.dumps(self.user))
        data = json.loads(response.get_data())
        token = data['token']
        response = self.client.put('/api/v1/meals/2', data=json.dumps(self.content), content_type='application/json',  headers={
            'Authorization': token})
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Enter a valid meal name and price", response.data)

    def test_account_update_meal_without_token(self):
        """Tests meal update without token"""
        self.client.post('/api/v1/auth/signup',
                         content_type='application/json', data=json.dumps(self.user))
        response = self.client.post(
            '/api/v1/auth/login', content_type='application/json', data=json.dumps(self.user))
        data = json.loads(response.get_data())
        token = data['token']
        response = self.client.put(
            '/api/v1/meals/1', data=json.dumps(self.content), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_account_delete_meal(self):
        """tests meal deletion"""
        self.client.post('/api/v1/auth/signup',
                         content_type='application/json', data=json.dumps(self.user))
        response = self.client.post(
            '/api/v1/auth/login', content_type='application/json', data=json.dumps(self.user))
        data = json.loads(response.get_data())
        token = data['token']
        self.client.post('/api/v1/meals', data=json.dumps(self.content),
                         content_type='application/json',  headers={'Authorization': token})
        response = self.client.delete(
            '/api/v1/meals/1', headers={'Authorization': token})
        self.assertEqual(response.status_code, 202)
        self.assertIn(b"The meal has been deleted", response.data)

    def test_account_delete_meal_twice(self):
        """"Tests double meal deletion"""
        self.client.post('/api/v1/auth/signup',
                         content_type='application/json', data=json.dumps(self.user))
        response = self.client.post(
            '/api/v1/auth/login', content_type='application/json', data=json.dumps(self.user))
        data = json.loads(response.get_data())
        token = data['token']
        self.client.post('/api/v1/meals', data=json.dumps(self.content),
                         content_type='application/json',  headers={'Authorization': token})
        self.client.delete('/api/v1/meals/1', headers={'Authorization': token})
        response = self.client.delete(
            '/api/v1/meals/1', headers={'Authorization': token})
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"The meal specified is not present", response.data)

    def test_account_delete_nonexistent_meal(self):
        """Tests deletion of non existent meal"""
        self.client.post('/api/v1/auth/signup',
                         content_type='application/json', data=json.dumps(self.user))
        response = self.client.post(
            '/api/v1/auth/login', content_type='application/json', data=json.dumps(self.user))
        data = json.loads(response.get_data())
        token = data['token']
        self.client.post('/api/v1/meals', data=json.dumps(self.content),
                         content_type='application/json',  headers={'Authorization': token})
        response = self.client.delete(
            '/api/v1/meals/54', headers={'Authorization': token})
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"The meal specified is not present", response.data)

    def test_account_delete_meal_without_token(self):
        """Tests deletion of meal without token"""
        self.client.post('/api/v1/auth/signup',
                         content_type='application/json', data=json.dumps(self.user))
        response = self.client.post(
            '/api/v1/auth/login', content_type='application/json', data=json.dumps(self.user))
        data = json.loads(response.get_data())
        token = data['token']
        self.client.post('/api/v1/meals', data=json.dumps(self.content),
                         content_type='application/json',  headers={'Authorization': token})
        response = self.client.delete('/api/v1/meals/1')
        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()
