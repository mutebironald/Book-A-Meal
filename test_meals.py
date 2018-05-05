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
        response = self.client.get('/api/v1/meals', headers={
                'Authorization': 'Basic ' + base64.b64encode(bytes('Ronald' + \
                ":" + 'Mutebi', 'ascii')).decode('ascii')
            })
        self.assertEqual(response.status_code, 200)

    def test_account_create_meal(self):
        content = {
            'meal_name':'Katogo',
            'price': 4000 
        }
        response = self.client.post('/api/v1/meals', data=content, headers={
                'Authorization': 'Basic ' + base64.b64encode(bytes('Ronald' + \
                ":" + 'Mutebi', 'ascii')).decode('ascii')
            })
        self.assertEqual(response.status_code, 200)

    def test_account_create_meal_without_data(self):
        content = {
            'meal_name':'',
            'price':''
        }
        response = self.client.post('/api/v1/meals', data=content, headers={
                'Authorization': 'Basic ' + base64.b64encode(bytes('Ronald' + \
                ":" + 'Mutebi', 'ascii')).decode('ascii')
            })
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Please enter a meal name", response.data)
 
    def test_account_update_meal(self):
        content = {
            'meal_name': 'Rice with gnuts',
            'meal_id': 1,
            'price': 2000
        }

        response = self.client.put('/api/v1/meals/1', data=content,  headers={
                'Authorization': 'Basic ' + base64.b64encode(bytes('Ronald' + \
                ":" + 'Mutebi', 'ascii')).decode('ascii')
            })
        response.content_type = 'multipart/form-data'    
        self.assertEqual(response.status_code, 200)

    def test_account_update_meal_without_data(self):
        
        content = {
            'meal_name': '',
            'price': 2000

        }
        response = self.client.put('/api/v1/meals/2', data=content,  headers={
                'Authorization': 'Basic ' + base64.b64encode(bytes('Ronald' + \
                ":" + 'Mutebi', 'ascii')).decode('ascii')
            })
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Please enter a meal name", response.data)

    def test_account_delete_meal(self):
        response = self.client.delete('/api/v1/meals/2',headers={
                'Authorization': 'Basic ' + base64.b64encode(bytes('Ronald' + \
                ":" + 'Mutebi', 'ascii')).decode('ascii')
            } )
        self.assertEqual(response.status_code, 202)
        self.assertIn(b"The meal has been deleted", response.data)

if __name__ == "__main__":
    unittest.main()