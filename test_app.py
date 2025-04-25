import unittest
from app import app  # Import the Flask app

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_home(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)  # Check if the status code is 200 OK

    def test_dashboard(self):
        response = self.app.get('/dashboard')
        self.assertIn(b"Welcome to the Dashboard", response.data)  # Check if the response contains the expected text
