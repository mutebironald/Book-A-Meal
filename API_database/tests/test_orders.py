import unittest
import os
import json
from app import create_app, db


class OrderTestCase(unittest.TestCase):
    """This class represents the order test case"""

    def setUp(self):
        self.app = create_app(config_name=os.getenv('APP_SETTINGS'))
        self.client = self.app.test_client
        self.order

    def setUp(self):
        """Defines the test variables and initializes the app."""
        self.app = create_app(config_name=os.getenv("APP_SETTINGS"))
        self.client = self.app.test_client
        self.meal = {"name": "Beef with Rice", "price": "4500"}
        self.menu = {"meal_id": 1}
        self.user_data = {
            "email": "mutebi@gmail.com",
            "password": "H1ack_it"
        }

        with self.app.app_context():
            # create all tables
            db.session.close()
            db.drop_all()
            db.create_all()

    def test_get_all_orders(self):
        """tests api ability to retrieve orders"""
        self.client().post("/auth/register", data=self.user_data)
        login_response = self.client().post("/auth/login", data=self.user_data)
        result = json.loads(login_response.data.decode())
        self.assertTrue(result["access_token"])
        self.client().post(
            "/api/v1/meals",
            data=self.meal,
            headers={
                "Authorization": result["access_token"]})
        response = self.client().post(
            "/api/v1/menu",
            data=self.menu,
            headers={
                "Authorization": result["access_token"]})
        order_response = self.client().post(
            "/api/"
        )
        pass

    def test_remove_order(self):
        """tests wether api can remove a specific order"""
        pass

    def tearDown(self):
        """teardown all initialized variables"""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


if __name__ == "__main__":
    unittest.main()
