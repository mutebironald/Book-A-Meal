"""unittests for menu in bookameal"""

import unittest
import json

from bookameal import app

class TestMeals(unittest.TestCase):
    def setUp(self):
        """Method which i run before every test"""
        self.client = app.test_client(self)

    def tearDown(self):
        """Called after each test method."""
        pass

    def test_get_menu(self):
        response = self.client.get('/api/v1/menu' )
        self.assertEqual(response.status_code, 200)
        

    def test_setup_menu(self):
        response = self.client.post('/api/v1/menu', content_type = "application/json", data = json.dumps(dict(meal_name="cassava", meal_id=3)))
        self.assertEqual(response.status_code, 201)
        


if __name__ == "__main__":
    unittest.main()
        
