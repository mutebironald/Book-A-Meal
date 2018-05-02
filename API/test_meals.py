"""unittests for meals in bookameal"""

import unittest
import json
import base64

from bookameal import app

class TestMeals(unittest.TestCase):
    def setUp(self):
        """Method which i run before every test"""
        self.client = app.test_client(self)

    def tearDown(self):
        """Called after each test method."""
        pass

    def test_get_meal(self):
        # headers={
        #         'Authorization': 'Basic ' + base64.b64encode('Ronald' + \
        #         ":" + 'Mutebi')
        #     }
        response = self.client.get('/api/v1/meals')
        self.assertEqual(response.status_code, 200)


    def test_account_create_meal(self):
        # headers={
        #         'Authorization': 'Basic ' + base64.b64encode('Ronald' + \
        #         ":" + 'Mutebi')
        #     }

        content = {
            'meal_name':'Katogo',
            'price': 4000 
        }
        response = self.client.post('/api/v1/meals', data=content)
        self.assertEqual(response.status_code, 200)

    def test_account_create_meal_without_data(self):
        content = {
            'meal_name':'',
            'price':''
        }
        response = self.client.post('/api/v1/meals', data=content)
        self.assertEqual(response.status_code, 400)

    def test_account_update_meal(self):
        content = {
            'meal_name': 'Rice with gnuts',
            'price': 2000

        }
        response = self.client.put('/api/v1/meals/2', data=content)
        self.assertEqual(response.status_code, 200)

    def test_account_update_meal_without_data(self):
        content = {
            'meal_name': '',
            'price': 2000

        }
        response = self.client.put('/api/v1/meals/2', data=content)
        self.assertEqual(response.status_code, 400)

    def test_account_delete_meal(self):
        response = self.client.delete('/api/v1/meals/2')
        self.assertEqual(response.status_code, 202)




if __name__ == "__main__":
    unittest.main()
        


# @app.route('/api/v1/meals')
# @basic_auth.required
# def account_get_meals():
#     """Enables meal retrieval for authenticated user"""
#     meals = DB.get_meals(current_user.get_id())
#     return jsonify({'MOCK_MEALS': meals}), 200

# @app.route('/api/v1/meals', methods=['POST'])
# @basic_auth.required
# def account_create_meal():
#     """Enables Authenticated user to create meals"""
#     meal_name = request.form.get('meal_name')
#     meal_id = DB.add_meal(meal_name, current_user.get_id())
#     DB.update_meal(meal_id, meal_name)
#     return make_response("You successfully created a meal", 200)



# @app.route('/api/v1/meals/<meal_id>', methods=["PUT"])
# @basic_auth.required
# def account_update_meal(meal_id):
#     """Authenticated user is ale to update meal"""
#     meal_name = request.form.get('mealname')
#     DB.update_meal(meal_id, meal_name)
#     return jsonify({'meals': MOCK_MEALS})




# @app.route('/api/v1/meals/<meal_id>', methods=["DELETE"])
# @basic_auth.required
# def account_delete_meal(meal_id):
#     """Authenticated user is able to delete particular meal"""
#     meal_id = request.form.get('meal_id')
#     DB.delete_meal(meal_id)
#     return make_response("The meal has been deleted", 202)



