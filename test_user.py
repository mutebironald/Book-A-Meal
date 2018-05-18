"""Unittests for User of Book-A-Meal"""

import unittest
import json
import base64

from api import app

class TestUser(unittest.TestCase):
    def setUp(self):
        """Method which i run before every test"""
        self.client = app.test_client(self)

    def tearDown(self):
        """Called after each test method."""
        pass

    def test_home(self):
        """Tests the home('/') route"""
        response = self.client.get('/')
        self.assertIn(b"Welcome to Book-A-Meal", response.data)

    def test_signup(self):
        """Tests that a user can be signed up"""
        user = {
            "email":"mutebironald4@gmail.com",
            "password":"lantern"
        }
        response = self.client.post('/api/v1/auth/signup', content_type = 'multipart/form-data', data=user)
        self.assertEqual(b"You are now registered", response.data)
        self.assertEqual(response.status_code, 201)

    def test_signup_with_all_fields_empty(self):
        """Tests if a user is signing up without data in fields"""
        user = {
            "email":"",
            "password":""
        }
        response = self.client.post('/api/v1/auth/signup', content_type = 'multipart/form-data', data=user)
        self.assertEqual(b"please enter a valid email address", response.data)
        self.assertEqual(response.status_code, 400)

    def test_signup_with_password_field_empty(self):
        """Tests if user is signing up with empty password field"""
        user = {
            "email":"ronald@gmail.com",
            "password":""
        }
        response = self.client.post('/api/v1/auth/signup', content_type = 'multipart/form-data', data=user)
        self.assertEqual(b"You must enter a password", response.data)
        self.assertEqual(response.status_code, 400)

    def test_signup_with_email_field_empty(self):
        """Test user is signing up with empty email field"""
        user = {
            "email":"",
            "password":"lantern"
        }
        response = self.client.post('/api/v1/auth/signup', content_type = 'multipart/form-data', data=user)
        self.assertEqual(b"please enter a valid email address", response.data)
        self.assertEqual(response.status_code, 400)

    def test_login_with_valid_credentials(self):
        """Test that a user can login"""
        user = {
            "email":"galabuzi@gmail.com",
            "password":"lantern"
        }
        self.client.post('/api/v1/auth/signup', content_type = 'multipart/form-data', data=user)
        response = self.client.post('/api/v1/auth/login', content_type='multipart/form-data', data = user)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"success!!, you are now logged in", response.data)
        

    def test_login_with_non_existent_email(self):
        """test login with un-registered email"""
        user = {
            "email":"myemail@gmail.com",
            "password":"lantern"
        }
        response = self.client.post('/api/v1/auth/login', content_type='multipart/form-data', data = user)
        self.assertEqual(response.status_code, 401)

    def test_login_with_empty_email_field(self):
        """Test login with empty email field"""
        user = {
            "email":"",
            "password":"lantern"
        }
        response = self.client.post('/api/v1/auth/login', content_type='multipart/form-data', data = user)
        self.assertEqual(response.status_code, 400)

    def test_login_with_password_field_empty(self):
        """Test login with empty password field"""
        user = {
            "email":"mutebi@gmail.com",
            "password":""
        }
        response = self.client.post('/api/v1/auth/login', content_type='multipart/form-data', data = user)
        self.assertEqual(response.status_code, 400)


    def test_login_with_empty_fields(self):
        """Test login with empty fields"""
        user = {
            "email":"",
            "password":""
        }
        response = self.client.post('/api/v1/auth/login', content_type='multipart/form-data', data = user)
        self.assertEqual(response.status_code, 400)

if __name__ == "__main__":
    unittest.main()
