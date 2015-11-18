import webapp2
import os
import jinja2
import logging
import google.appengine.ext.db
import webtest
from pages.alertincident import alertincident
import unittest
from google.appengine.ext import testbed

class AppTest(unittest.TestCase):

  def setUp(self):
    app = webapp2.WSGIApplication([('/alertincident', alertincident)])
    self.testapp = webtest.TestApp(app)
    self.testbed = testbed.Testbed()
    self.testbed.activate()
    self.testbed.init_datastore_v3_stub()

  def tearDown(self):
     self.testbed.deactivate()

  def testAlertIncidentHandler(self):
    res = self.testapp.get('/alertincident')
    self.assertEqual(res.status_int, 200)
