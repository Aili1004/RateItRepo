import webapp2
import os
import jinja2
import logging
import google.appengine.ext.db
import webtest
from pages.prioritypassengers import prioritypassengers
import unittest
from google.appengine.ext import testbed

class AppTest(unittest.TestCase):

  def setUp(self):
    app = webapp2.WSGIApplication([('/operator/classifypassengers/prioritypassengers', prioritypassengers)])
    self.testapp = webtest.TestApp(app)
    self.testbed = testbed.Testbed()
    self.testbed.activate()
    self.testbed.init_datastore_v3_stub()

  def tearDown(self):
     self.testbed.deactivate()

  def testOperatorPriorityPassengersHandler2(self):
    res = self.testapp.get('/operator/classifypassengers/prioritypassengers')
    self.assertEqual(res.status_int, 200)
