import unittest
import json

from app import app

class TestMenu(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client(self)

    def test_menu_creation(self):
        """Tests that a meal or meals can be added to the menu"""
        self.client.post('api/v1/meals', content_type='application/json', data=json.dumps(dict(meal_name='Rice and Fish', price=6000)))
        self.client.post('api/v1/meals', content_type='application/json', data=json.dumps(dict(meal_name='Beef with Matooke', price=3000)))
        response = self.client.post('/api/v1/menu/3')
        self.assertEqual(response.status_code, 201)
        self.assertIn(u'Successfully added to the menu', response.data)

    def test_meal_uniqueness_on_menu(self):
        """Tests that there isn't a duplicate meal on the menu"""
        self.client.post('/api/v1/meals', content_type='application/json', data=json.dumps(dict(meal_name='Macroni and Chips', price=4600)))
        self.client.post('api/v1/meals', content_type='application/json',data=json.dumps(dict(meal_name='Marangwe with ughali', price=3550)))
        
        self.client.post('api/v1/menu/1')

        response = self.client.post('/api/v1/menu/1')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(u'Meal already exists in menu', response.data)

    def test_get_menu(self):
        """Tests that a menu can be retrieved"""
        self.client.post('api/v1/meals', content_type='application/json', data=json.dumps(dict(meal_name='Chicken with pilao', price=9000)))
        self.client.post('api/v1/meals/', content_type='application/json', data=json.dumps(dict(meal_name='Beef with fries', price=4500)))
        self.client.post('api/v1/meals', content_type='application/json', data=json.dumps(dict(meal_name='Cassava with Meat', price=3000)))
        self.client.post('api/v1/meals', content_type='application/json', data=json.dumps(dict(meal_name='Katoogo', price=2000)))

        self.client.post('api/v1/menu/7')
        response = self.client.get('api/v1/menu/')
        self.assertIn(u'Cassava with meat', response.data)

if __name__ =='__main__':
    unittest.main()
