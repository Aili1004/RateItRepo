import webapp2
import os
import jinja2
import logging
import google.appengine.ext.db
import webtest
from pages.classifypassengers import classifypassengers
import unittest
from google.appengine.ext import testbed

class AppTest(unittest.TestCase):

  def setUp(self):
    app = webapp2.WSGIApplication([('/operator/classifypassengers', classifypassengers)])
    self.testapp = webtest.TestApp(app)
    self.testbed = testbed.Testbed()
    self.testbed.activate()
    self.testbed.init_datastore_v3_stub()

  def tearDown(self):
     self.testbed.deactivate()

  def testOperatorClassifyPassengersHandler2(self):
    res = self.testapp.get('/operator/classifypassengers')
    self.assertEqual(res.status_int, 200)
