import webapp2
import webtest
import unittest
from Hello import HelloWorldHandler

class AppTest(unittest.TestCase):
    def setUp(self):
        # Create a WSGI application.
        app = webapp2.WSGIApplication([('/', HelloWorldHandler)])
        self.testapp = webtest.TestApp(app)

    # Test the handler.
    def testHelloWorldHandler(self):
        response = self.testapp.get('/')
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.normal_body, 'Hello World!')
        self.assertEqual(response.content_type, 'text/plain')