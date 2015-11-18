import webapp2
import os
import jinja2
import logging
import google.appengine.ext.db
import webtest
from pages.choosebus import choosebus
import unittest
from google.appengine.ext import testbed

class AppTest(unittest.TestCase):

  def setUp(self):
    app = webapp2.WSGIApplication([('/choosebus', choosebus)])
    self.testapp = webtest.TestApp(app)
    self.testbed = testbed.Testbed()
    self.testbed.activate()
    self.testbed.init_datastore_v3_stub()

  def tearDown(self):
     self.testbed.deactivate()

  def testChooseBusHandler(self):
    res = self.testapp.get('/choosebus')
    self.assertEqual(res.status_int, 200)
