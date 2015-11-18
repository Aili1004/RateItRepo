import webapp2
import os
import jinja2
import logging
import google.appengine.ext.db
import webtest
from pages.about import about
import unittest
from google.appengine.ext import testbed

class AppTest(unittest.TestCase):

  def setUp(self):
    app = webapp2.WSGIApplication([('/about', about)])
    self.testapp = webtest.TestApp(app)
    self.testbed = testbed.Testbed()
    self.testbed.activate()

  def tearDown(self):
     self.testbed.deactivate()

  def testAboutHandler(self):
    res = self.testapp.get('/about')
    self.assertEqual(res.status_int, 200)
