import unittest
from app import app

class BoltRouteTests(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_bolt_page_status_code(self):
        response = self.app.get('/bolt')
        self.assertEqual(response.status_code, 200)

    def test_bolt_page_content(self):
        response = self.app.get('/bolt')
        self.assertIn(b'3D Bolt Stress Simulation', response.data)
        self.assertIn(b'three.module.js', response.data)

if __name__ == '__main__':
    unittest.main()
