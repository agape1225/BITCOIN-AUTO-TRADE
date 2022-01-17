import unittest, inspect
from db.mongodb.mongodb_handler import MongoDBHandler
class MongoDBHandlerTestCase(unittest.TestCase):
    def setUp(self):
        self.mongodb = MongoDBHandler("local", "coiner", "price_info")
        self.mongodb.delete_items({})
        docs = [
            {"currency": "btc", "price": 10000},
            {"currency": "eth", "price": 1000},
            {"currency": "xrp", "price": 100},
            {"currency": "btc", "price": 20000},
            {"currency": "eth", "price": 2000},
            {"currency": "xrp", "price": 200},
        ]

    def tearDown(self):
        pass

    if __name__ == "__main__":
        unittest.main()