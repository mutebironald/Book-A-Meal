import unittest
import json

from app import app

class TestMeal(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client(self)

    def test_meal_creation(self):
        """tests that a meal option can be successfully added"""
        response = self.client.post('api/v1/meals/', data=json.dumps(dict(meal_name='Beef with rice', price='5000')))
        response.content_type = 'application/json'

        result = json.loads(response.data.decode())
        self.assertIn(u'Successfully added meal option', result['message'])
        self.assertEqual(response.status_code, 201)

    def test_valid_meal_creation(self):
        """tests that a meal option cannot be added if the price is passed as astring
        instead of an integer"""
        response = self.client.post('api/v1/meals', data=json.dumps(dict(meal_name='Beef with rice',price='wresy3')))
        response.content_type = 'application/json'
        result = json.loads(response.data.decode())

        self.assertIn(u'Meal option already exists, try another', result['message'])
        self.assertEqual(response.status_code, 401)

    def test_ability_to_get_all_meals(self):
        """Tests ability to get all existing meal options"""
        self.client.post('api/v1/meals', content_type='application/json', data=json.dumps(dict(meal_name='Posho with Beans', price=3000)))
        self.client.post('api/v1/meals', content_type='application/json', data=json.dumps(dict(meal_name='Matooke with Gnuts',price=3500)))

        response = self.client.get('api/v1/meals/')

        result = json.loads(response.data.decode())
        self.assertEqual(len(result['meals']), 2)

    def test_meal_update(self):
        """Tests that a meal option can be updated"""
        self.client.post('api/v1/meals', content_type='application/json', data=json.dumps(dict(meal_name='Chicken with pilao', price=9000)))
        self.client.post('api/v1/meals/', content_type='application/json', data=json.dumps(dict(meal_name='Beef with fries', price=4500)))
        self.client.post('api/v1/meals', content_type='application/json', data=json.dumps(dict(meal_name='Cassava with Meat', price=3000)))
        self.client.post('api/v1/meals', content_type='application/json', data=json.dumps(dict(meal_name='Katoogo', price=2000)))

        response = self.client.put('/api/v1/meals/4', content_type='application/json', data=json.dumps(dict(meal_name='Beans with chapati', price=1500)))
        self.assertEqual(response.status_code, 201)
        self.assertIn(u'Successfully updated meal', response.data)

    def test_wrong_update(self):
        """test that a non existent meal option cannot be updated"""
        self.client.post('api/v1/meals', content_type='application/json', data=json.dumps(dict(meal_name='Chicken with pilao', price=9000)))
        self.client.post('api/v1/meals/', content_type='application/json', data=json.dumps(dict(meal_name='Beef with fries', price=4500)))
        self.client.post('api/v1/meals', content_type='application/json', data=json.dumps(dict(meal_name='Cassava with Meat', price=3000)))
        self.client.post('api/v1/meals', content_type='application/json', data=json.dumps(dict(meal_name='Katoogo', price=2000)))

        response = self.client.put('/api/v1/meals/7', content_type='application/json', data=json.dumps(dict(meal_name='Chaps and Sumbi', price=2000)))
        self.assertEqual(response.status_code, 404)
        self.assertIn(u'Meal option does not exist', response.data)

    def test_meal_deletion(self):
        """Tests that a meal can be deleted"""
        self.client.post('api/v1/meals', content_type='application/json', data=json.dumps(dict(meal_name='Chicken with pilao', price=9000)))
        self.client.post('api/v1/meals/', content_type='application/json', data=json.dumps(dict(meal_name='Beef with fries', price=4500)))
        self.client.post('api/v1/meals', content_type='application/json', data=json.dumps(dict(meal_name='Cassava with Meat', price=3000)))
        self.client.post('api/v1/meals', content_type='application/json', data=json.dumps(dict(meal_name='Katoogo', price=2000)))

        response = self.client.delete('api/v1/meals/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn(u'Successfully deleted meal', response.data)

    def test_failed_meal_deletion(self):
        """Test deletion of a meal that is not in the available meals"""
        self.client.post('api/v1/meals', content_type='application/json', data=json.dumps(dict(meal_name='Chicken with pilao', price=9000)))
        self.client.post('api/v1/meals/', content_type='application/json', data=json.dumps(dict(meal_name='Beef with fries', price=4500)))
        self.client.post('api/v1/meals', content_type='application/json', data=json.dumps(dict(meal_name='Cassava with Meat', price=3000)))
        self.client.post('api/v1/meals', content_type='application/json', data=json.dumps(dict(meal_name='Katoogo', price=2000)))

        response = self.client.delete('api/v1/meals/9')
        self.assertEqual(response.status_code, 401)
        self.assertIn(u'Failed to delete meal', response.data)

if __name__ == '__main__':
    unittest.main()


