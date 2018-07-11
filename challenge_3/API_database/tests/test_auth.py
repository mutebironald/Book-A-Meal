import unittest
import os
import json
from app import create_app, db


class AuthTestCase(unittest.TestCase):
    """test case for the authentication blueprint."""

    def setUp(self):
        """Set up test variables."""
        self.app = create_app(config_name=os.getenv('APP_SETTINGS'))
        self.client = self.app.test_client
        self.user_data = {
            "email": "ronald@gmail.com",
            "password": "U1nhackable"
        }

        with self.app.app_context():
            # create all tables
            db.session.close()
            db.drop_all()
            db.create_all()

    def test_registration(self):
        """Test user registration works correctly."""
        response = self.client().post('/auth/register', data=self.user_data)
        result = json.loads(response.data.decode())
        self.assertEqual(result["message"], "You registered successfully.")
        self.assertEqual(response.status_code, 201)

    def test_already_registered_user(self):
        """Test that a user cannot be registered twice."""
        self.client().post("/auth/register", data=self.user_data)
        response = self.client().post("/auth/register", data=self.user_data)
        result = json.loads(response.data.decode())
        self.assertEqual(
            result["message"],
            "User already exists. Please login.")

    def test_registration_with_token_like_password(self):
        """tests wether a user can register with invalid password"""
        user_data = {
            "email": "ronald@gmail.com",
            "password": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1MzA5\
            ODAyNDIsInN1YiI6Nn0.FDWEgSrNXmt6r_8ocwVbMRbU1h9u76w-ZhQ71SoJJus"
        }
        response = self.client().post("/auth/register", data=user_data)
        result = json.loads(response.data.decode())
        self.assertEqual(
            result["message"],
            "Password must contain 1 capital letter and 1 number")

    def test_user_login(self):
        """Test registered user can login."""
        self.client().post("/auth/register", data=self.user_data)
        login_response = self.client().post("/auth/login", data=self.user_data)
        result = json.loads(login_response.data.decode())
        self.assertEqual(result["message"], "You logged in successfully.")
        self.assertEqual(login_response.status_code, 200)
        self.assertTrue(result["access_token"])

    def test_non_registered_user_login(self):
        """Test non registered users cannot login."""
        not_a_user = {
            "email": "hacker@gmail.com",
            "password": "badguy"
        }
        response = self.client().post("/auth/login", data=not_a_user)
        result = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            result["message"],
            "Invalid email or password, Please try again")
