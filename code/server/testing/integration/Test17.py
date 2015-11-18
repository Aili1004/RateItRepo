import webapp2
import os
import jinja2
import logging
import google.appengine.ext.db
import webtest
from pages.operator_upload_gtfs import operator_upload_gtfs
import unittest
from google.appengine.ext import testbed

class AppTest(unittest.TestCase):

  def setUp(self):
    app = webapp2.WSGIApplication([('/operator/upload_gtfs', operator_upload_gtfs)])
    self.testapp = webtest.TestApp(app)
    self.testbed = testbed.Testbed()
    self.testbed.activate()
    self.testbed.init_datastore_v3_stub()
    self.testbed.init_blobstore_stub()

  def tearDown(self):
     self.testbed.deactivate()

  def testOperatorUploadGTFSHandler2(self):
    res = self.testapp.get('/operator/upload_gtfs')
    self.assertEqual(res.status_int, 200)
