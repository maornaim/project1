import unittest
from app import app, client, db, collection
from bson.objectid import ObjectId

class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        # Setup before each test
        self.app = app.test_client()
        self.app.testing = True

        # Clean the database before each test
        collection.delete_many({})

    def tearDown(self):
        # Cleanup after each test
        collection.delete_many({})

    def test_add_stock(self):
        response = self.app.post('/add_stock', data=dict(
            name="TestStock",
            monthly_prices="100,150,200"
        ), follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        stock = collection.find_one({"name": "TestStock"})
        self.assertIsNotNone(stock)
        self.assertEqual(stock["name"], "TestStock")
        self.assertEqual(stock["monthly_prices"], [100, 150, 200])

    def test_get_stocks(self):
        collection.insert_one({
            "name": "TestStock",
            "monthly_prices": [100, 150, 200]
        })

        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"TestStock", response.data)
    
    def test_calculate_changes(self):
        stock_id = collection.insert_one({
            "name": "TestStock",
            "monthly_prices": [100, 150, 200]
        }).inserted_id

        response = self.app.get(f'/calculate_changes/{stock_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Month 1: Change = 50", response.data)
        self.assertIn(b"Month 2: Change = 50", response.data)

if __name__ == '__main__':
    unittest.main()
