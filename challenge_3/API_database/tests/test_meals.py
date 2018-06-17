import unittest
import os
import json
from app import create_app, db

class MealsTestCase(unittest.TestCase):
    """This class represents the meals test case"""

    def setUp(self):
        """Defines the test variables and initializes the app."""
        self.app = create_app(config_name=os.getenv('APP_SETTINGS'))
        self.client = self.app.test_client
        self.meal = {'name':'bae', 'price':'3000'}
        self.user_data = {
            'email': 'mutebi@gmail.com',
            'password': 'hack_it'
            }

        with self.app.app_context():
            #create all tables
            db.session.close()
            db.drop_all()
            db.create_all()

    def register_user(self, email='mail@gmail.com', password='epic'):
        """This helper method helps register a test user."""
        user_data = {
            'email': email,
            'password': password
        }
        return self.client().post('/auth/register', data=user_data)

    def login_user(self, email='mail@gmail.com', password='apic'):
        """This helper method helps log in a test user."""
        user_data={
            'email':email,
            'password':password
        }
        return self.client().post('/auth/login', data=user_data)

    def test_meal_creation(self):
        """Test API can create a meal"""
        #First signup
        response = self.client().post('/api/v1/auth/signup', data=self.user_data)
        self.assertEqual(response.status_code, 201)
        #login
        login_response = self.client().post('/api/v1/auth/login', data=self.user_data)
        self.assertEqual(login_response.status_code, 200)
        result = json.loads(login_response.data.decode())
        self.assertTrue(result['access_token'])
        
        response = self.client().post('/api/v1/meals', data=self.meal, headers={"Authorization": result['access_token'] })
        self.assertEqual(response.status_code, 201)
        self.assertIn('bae', str(response.data))

    def test_api_can_get_all_meals(self):
        """Test API can get a meal"""
        response = self.client().post('/api/v1/auth/signup', data=self.user_data)
        self.assertEqual(response.status_code, 201)
        #login
        login_response = self.client().post('/api/v1/auth/login', data=self.user_data)
        self.assertEqual(login_response.status_code, 200)
        result = json.loads(login_response.data.decode())
        self.assertTrue(result['access_token'])
        #post meals
        response = self.client().post('/api/v1/meals', data=self.meal, headers={"Authorization": result['access_token'] })
        self.assertEqual(response.status_code, 201)
        response = self.client().get('/api/v1/meals', headers={"Authorization": result['access_token'] })
        self.assertEqual(response.status_code, 200)


    def test_api_can_get_meal_by_id(self):
        """Test API can get particular meal"""
        #First signup
        response = self.client().post('/api/v1/auth/signup', data=self.user_data)
        self.assertEqual(response.status_code, 201)
        #login
        login_response = self.client().post('/api/v1/auth/login', data=self.user_data)
        self.assertEqual(login_response.status_code, 200)
        result = json.loads(login_response.data.decode())
        self.assertTrue(result['access_token'])
        response = self.client().post('/api/v1/meals', data=self.meal, headers={"Authorization": result['access_token'] })
        self.assertEqual(response.status_code, 201)
        result = self.client().get('/api/v1/meals/1', headers={"Authorization": result['access_token'] })
        self.assertEqual(result.status_code, 200)


    def test_meal_can_be_edited(self):
        """Test API can edit an existing meal"""
        #First signup
        response = self.client().post('/api/v1/auth/signup', data=self.user_data)
        self.assertEqual(response.status_code, 201)
        #login
        login_response = self.client().post('/api/v1/auth/login', data=self.user_data)
        self.assertEqual(login_response.status_code, 200)
        result = json.loads(login_response.data.decode())
        self.assertTrue(result['access_token'])

        response = self.client().post('/api/v1/meals', data={'name':'chips', 'price':'5000'},
                                      headers={"Authorization": result['access_token'] })
        self.assertEqual(response.status_code, 201)
        response = self.client().put(
            '/api/v1/meals/1',
            data={
                'name':'macroni', 'price':'2500'
                }, headers={"Authorization": result['access_token'] })
        self.assertEqual(response.status_code, 200)
        results = self.client().get('/api/v1/meals', headers={"Authorization": result['access_token'] })
        self.assertIn('macroni', str(results.data))

    def test_meal_can_be_deleted(self):
        """Test API can delete an existing meal"""
        #First signup
        response = self.client().post('/api/v1/auth/signup', data=self.user_data)
        self.assertEqual(response.status_code, 201)
        #login
        login_response = self.client().post('/api/v1/auth/login', data=self.user_data)
        self.assertEqual(login_response.status_code, 200)
        result = json.loads(login_response.data.decode())
        self.assertTrue(result['access_token'])
        
        response = self.client().post(
            '/api/v1/meals',
            data={'name':'pam', 'price':'3200'}, headers={"Authorization": result['access_token']})
        self.assertEqual(response.status_code, 201)
        response = self.client().delete('/api/v1/meals/1', headers={'Authorization': result['access_token']})
        self.assertEqual(response.status_code, 200)
        result = self.client().get('/api/v1/meals', headers={'Authorization': result['access_token']})
        self.assertEqual(result.status_code, 400)

    def tearDown(self):
        """teardown all initialized variables"""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

            

if __name__ == "__main__":
    unittest.main()
        