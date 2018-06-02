import unittest
import json
from bookameal import app, db

class UsersTestCase(unittest.TestCase):
    """Test case for the authentication blueprint"""

    def setUp(self):
        """Set up the test variables"""
        self.app = app
        self.client = self.app.test_client

        self.user_data = {
            'email': 'mutebi@gmail.com',
            'password': 'hack_it'
            }

        with self.app.app_context():
            db.session.close()
            db.drop_all()
            db.create_all()


    def test_signup(self):
        """Test user is able to signup"""
        response = self.client().post('/api/v1/auth/signup', data=self.user_data)
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], "You are now registered")
        self.assertEqual(response.status_code, 201)


    def test_double_signup(self):
        """Test that a particular user can only signup once"""
        response = self.client().post('api/v1/auth/signup', data=self.user_data)
        self.assertEqual(response.status_code, 201)
        second_response = self.client().post('api/v1/auth/signup', data=self.user_data)
        self.assertEqual(second_response.status_code, 202)

        #result = json.loads(second_response.data.decode())
        
        #self.assertEqual(
            #result['message'], "The user already exists")

    def test_user_login(self):
        """Tests that a signed up user can e logged in"""
        response = self.client().post('api/v1/auth/signup', data=self.user_data)
        self.assertEqual(response.status_code, 201)
        login_response = self.client().post('/api/v1/auth/login', data=self.user_data)
        result = json.loads(login_response.data.decode())
        self.assertEqual(result['message'], 'You logged in successfully.')

        self.assertEqual(login_response.status_code, 200)
        self.assertTrue(result['access_token'])

    def test_non_registered_user_login(self):
        """Test that a user who did not sign up user cannot login"""

        anonymous_user = {
            'email': 'anonymous@gmail.com',
            'password': 'insanity'
            }
        response = self.client().post('api/v1/auth/login', data=anonymous_user)
        result = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            result['message'], 'Invalid email or password')

if __name__ == "__main__":
    unittest.main()
