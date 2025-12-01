import unittest
from app import app
import json

class FlaskAppTests(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_home_status_code(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_home_content(self):
        response = self.app.get('/')
        self.assertIn(b'Welcome', response.data)
        self.assertIn(b'What\'s your name?', response.data)

    def test_greet_user_json(self):
        # Test the AJAX JSON endpoint
        response = self.app.post('/',
                                 data=json.dumps({'name': 'Tester'}),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.is_json)
        self.assertEqual(response.json['greeting'], 'Hello, Tester!')

    def test_greet_user_fallback(self):
        # Test the standard form submission fallback
        response = self.app.post('/', data=dict(name="Tester"))
        self.assertEqual(response.status_code, 200)
        # Check if the greeting is rendered in the HTML
        self.assertIn(b'Tester', response.data)
        self.assertIn(b'Hello,', response.data)

if __name__ == '__main__':
    unittest.main()
