import unittest
import os
import json
from bookameal import app, db


class OrderTestCase(unittest.Testcase):
    """This class represents the order test case"""
    def setUp(self):
        self.app = app
    self.client = self.app.test_client
    self.order 


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
                  
