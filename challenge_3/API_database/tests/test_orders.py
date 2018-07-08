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
        # self.meal = {'name':'bae', 'price':'3000'}
        # self.menu = {'name': 'local foods', 'day': 'Monday'}
        self.user_data = {
            "email": "mutebi@gmail.com",
            "password": "hack_it"
        }

        with self.app.app_context():
            # create all tables
            db.session.close()
            db.drop_all()
            db.create_all()

    def test_get_all_orders(self):
        """tests api ability to retrieve orders"""
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
