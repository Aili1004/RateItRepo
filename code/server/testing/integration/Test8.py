import webapp2
import os
import jinja2
import logging
import google.appengine.ext.db
import webtest
from pages.addbus import addbus
import unittest
from google.appengine.ext import testbed

class AppTest(unittest.TestCase):

  def setUp(self):
    app = webapp2.WSGIApplication([('/addbus', addbus)])
    self.testapp = webtest.TestApp(app)
    self.testbed = testbed.Testbed()
    self.testbed.activate()
    self.testbed.init_datastore_v3_stub()

  def tearDown(self):
     self.testbed.deactivate()

  def testAddBusHandler(self):
    res = self.testapp.get('/addbus')
    self.assertEqual(res.status_int, 200)
