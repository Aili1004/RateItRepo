import webapp2
import os
import jinja2
import logging
import google.appengine.ext.db
import webtest
from pages.verifyalert import verifyalert
import unittest
from google.appengine.ext import testbed

class AppTest(unittest.TestCase):

  def setUp(self):
    app = webapp2.WSGIApplication([('/verifyalert', verifyalert)])
    self.testapp = webtest.TestApp(app)
    self.testbed = testbed.Testbed()
    self.testbed.activate()
    self.testbed.init_datastore_v3_stub()

  def tearDown(self):
     self.testbed.deactivate()

  def testVerifyAlertHandler(self):
    res = self.testapp.get('/verifyalert')
    self.assertEqual(res.status_int, 200)
