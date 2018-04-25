"""unittests for Book-A-Meal"""

import unittest
import json
import app

class TestUsers(unittest.TestCase):
    """This class represents a user test case"""
    def setUp(self):
        """Called before each test method"""
        self.client = app.test_client()

    def test_successful_signup(self):
        """Tests that a user can be signed in"""
        response = self.client.post('/auth/signup', data=json.dumps(dict(email='papvert@gmail.com',
                                    password='lantern')))
        response.content_type = 'application/json'
        self.assertIn(u"Successfully signed up", response.data)
        self.assertEqual(response.status_code, 201)

    def test_unique_user_signup(self):
        """Tests that a unique user can be added"""
        self.client.post('/auth/signup',content_type='application/json', data=json.dumps(dict(email='ronald@gmail.com',
                                                              password='lighten')))

        response = self.client.post('/auth/signup', content_type='application/json',
                                     data=json.dumps(dict(email='ronald@gmail.com', password='lighten')))
        self.assertIn(u"User already exists", response.data)
        self.assertEqual(response.status_code, 401)

    def test_wrong_format_credentials_signup(self):
        """Tests that a user cannot be added with wrong email format"""

        response = self.client.post('/auth/signup',data=json.dumps(dict(email='ronald@@gmail.com',
                                                                        password='lighten')))
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], u'''Repetition of "@" is not allowed''')
        self.assertEqual(response.status_code, 422)

    def test_correct_credential_login(self):
        """Tests that correct credentials are used during login"""
        self.client.post('/auth/signup',content_type='application/json',
                         data=json.dumps(dict(email="ronald@gmail.com",password="lighten")))
        login = self.client.post('/auth/login',content_type='application/json', data=json.dumps(dict(email="ronald@gmail.com",
                                                                     password="lighten")))
        result = json.loads(login.data.decode())
        self.assertIn(u'token',result)
        self.assertEqual(login.status_code, 200)

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
        