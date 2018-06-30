import unittest
import os
import json
from app import create_app, db

class MenuTestCase(unittest.TestCase):
    """This class represents the menu test case"""
    def setUp(self):
        """Defines the test variables and initializes the app."""
        self.app = create_app(config_name=os.getenv('APP_SETTINGS'))
        self.client = self.app.test_client
        self.menu = {'name': 'local foods', 'day': 'Monday'}
        self.user_data = {
            'email': 'mutebi@gmail.com',
            'password': 'hack_it'
            }

        with self.app.app_context():
            #create all tables
            db.session.close()
            db.drop_all()
            db.create_all()

    def test_setup_menu(self):
        self.client().post('/auth/register', data=self.user_data)
        login_response = self.client().post('/auth/login', data=self.user_data)
        result = json.loads(login_response.data.decode())
        self.assertTrue(result['access_token'])
        response = self.client().post('/api/v1/menu', data=self.menu, headers={"Authorization": result['access_token'] })
        self.assertEqual(response.status_code, 201)



    def test_get_menu(self):
        self.client().post('/auth/register', data=self.user_data)
        login_response = self.client().post('/auth/login', data=self.user_data)
        result = json.loads(login_response.data.decode())
        self.assertTrue(result['access_token'])
        self.client().post('/api/v1/menu', data=self.menu, headers={"Authorization": result['access_token'] })
        response = self.client().get('/api/v1/menu', headers={"Authorization": result['access_token'] })
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        """teardown all initialized variables"""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

if __name__ == "__main__":
    unittest.main()
