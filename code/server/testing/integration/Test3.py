import webapp2
import os
import jinja2
import logging
import google.appengine.ext.db
import webtest
from pages.home import home
import unittest
from google.appengine.ext import testbed

class AppTest(unittest.TestCase):

  def setUp(self):
    app = webapp2.WSGIApplication([('/', home)])
    self.testapp = webtest.TestApp(app)
    self.testbed = testbed.Testbed()
    self.testbed.activate()
    self.testbed.init_datastore_v3_stub()

  def tearDown(self):
     self.testbed.deactivate()

  def testHomeHandler(self):
    res = self.testapp.get('/')
    self.assertEqual(res.status_int, 200)
