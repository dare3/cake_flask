import unittest
import json
from app import app, db, Cupcake

class CupcakeTestCase(unittest.TestCase):
    def setUp(self):
        """Set up a test client and an in-memory database."""
        self.app = app
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use an in-memory database for testing
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()  # Create the database tables

            # Add a sample cupcake for testing
            cupcake = Cupcake(
                flavor='Chocolate',
                size='Medium',
                rating=4.5,
                image='https://tinyurl.com/demo-cupcake'
            )
            db.session.add(cupcake)
            db.session.commit()

    def tearDown(self):
        """Clean up the database after each test."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_patch_cupcake(self):
        """Test updating a cupcake."""
        response = self.client.patch('/api/cupcakes/1', json={
            'flavor': 'Chocolate Mint',
            'size': 'Large',
            'rating': 4.9,
            'image': 'https://example.com/chocolate-mint-cupcake.jpg'
        })
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['cupcake']['flavor'], 'Chocolate Mint')
        self.assertEqual(data['cupcake']['size'], 'Large')
        self.assertEqual(data['cupcake']['rating'], 4.9)
        self.assertEqual(data['cupcake']['image'], 'https://example.com/chocolate-mint-cupcake.jpg')

    def test_patch_cupcake_not_found(self):
        """Test updating a cupcake that does not exist."""
        response = self.client.patch('/api/cupcakes/999', json={
            'flavor': 'Strawberry',
            'size': 'Medium',
            'rating': 4.7,
            'image': 'https://example.com/strawberry-cupcake.jpg'
        })
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'Cupcake not found')

    def test_delete_cupcake(self):
        """Test deleting a cupcake."""
        response = self.client.delete('/api/cupcakes/1')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'Deleted')

    def test_delete_cupcake_not_found(self):
        """Test deleting a cupcake that does not exist."""
        response = self.client.delete('/api/cupcakes/999')
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'Cupcake not found')

if __name__ == '__main__':
    unittest.main()
