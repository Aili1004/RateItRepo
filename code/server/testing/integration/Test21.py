import webapp2
import os
import jinja2
import logging
import google.appengine.ext.db
import webtest
from pages.alertincidentpassengers import alertincidentpassengers
import unittest
from google.appengine.ext import testbed

class AppTest(unittest.TestCase):

  def setUp(self):
    app = webapp2.WSGIApplication([('/operator/classifypassengers/alertincidentpassengers', alertincidentpassengers)])
    self.testapp = webtest.TestApp(app)
    self.testbed = testbed.Testbed()
    self.testbed.activate()
    self.testbed.init_datastore_v3_stub()

  def tearDown(self):
     self.testbed.deactivate()

  def testOperatorAlertIncidentPassengersHandler2(self):
    res = self.testapp.get('/operator/classifypassengers/alertincidentpassengers')
    self.assertEqual(res.status_int, 200)
