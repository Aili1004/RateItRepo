import webapp2
import os
import jinja2
import logging
import google.appengine.ext.db
import webtest
from pages.operatorhome import operatorhome
import unittest
from google.appengine.ext import testbed

class AppTest(unittest.TestCase):

  def setUp(self):
    app = webapp2.WSGIApplication([('/operator/home', operatorhome)])
    self.testapp = webtest.TestApp(app)
    self.testbed = testbed.Testbed()
    self.testbed.activate()

  def tearDown(self):
     self.testbed.deactivate()

  def testOperatorHomeHandler2(self):
    res = self.testapp.get('/operator/home')
    self.assertEqual(res.status_int, 200)
