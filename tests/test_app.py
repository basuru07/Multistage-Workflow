# tests/test_app.py
import unittest
import json
from urllib.request import urlopen
from urllib.error import URLError
import threading
import time
from app import HTTPServer, SimpleHandler

class TestApp(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        # Start server in background for testing
        cls.server = HTTPServer(('localhost', 9999), SimpleHandler)
        cls.server_thread = threading.Thread(target=cls.server.serve_forever)
        cls.server_thread.daemon = True
        cls.server_thread.start()
        time.sleep(0.1)  # Give server time to start
    
    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
    
    def test_home_endpoint(self):
        try:
            response = urlopen('http://localhost:9999/')
            data = json.loads(response.read().decode())
            self.assertEqual(data['message'], 'Hello World!')
            self.assertEqual(data['version'], '1.0.0')
        except URLError:
            self.fail("Could not connect to server")
    
    def test_health_endpoint(self):
        try:
            response = urlopen('http://localhost:9999/health')
            data = json.loads(response.read().decode())
            self.assertEqual(data['status'], 'OK')
        except URLError:
            self.fail("Could not connect to server")
    
    def test_status_endpoint(self):
        try:
            response = urlopen('http://localhost:9999/api/status')
            data = json.loads(response.read().decode())
            self.assertIn('python_version', data)
            self.assertEqual(data['version'], '1.0.0')
        except URLError:
            self.fail("Could not connect to server")

if __name__ == '__main__':
    unittest.main()