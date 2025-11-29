import unittest
from app import app

class FlaskAppTests(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_home_status_code(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_home_content(self):
        response = self.app.get('/')
        self.assertIn(b'Hello World App', response.data)
        self.assertIn(b'Enter your name:', response.data)

    def test_greet_user(self):
        response = self.app.post('/', data=dict(name="Tester"))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Hello, Tester!', response.data)

if __name__ == '__main__':
    unittest.main()
