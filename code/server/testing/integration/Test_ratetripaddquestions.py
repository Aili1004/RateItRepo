import webapp2
import os
import jinja2
import logging
import google.appengine.ext.db
import webtest
from pages.ratetrip import ratetrip
import unittest
import protocol.submit_trip_rating
from google.appengine.ext import testbed

class AppTest(unittest.TestCase):

	def setUp(self):
		app = webapp2.WSGIApplication([('/addquestions/', addquestions)])
		self.testapp = webtest.TestApp(app)
		self.testbed = testbed.Testbed()
		self.testbed.activate()
		self.testbed.init_datastore_v3_stub()

	def tearDown(self):
		self.testbed.deactivate()

	def testAddQuestionsHandler(self):
		res = self.testapp.get('/addquestions/')
		self.assertEqual(res.status_int, 200)
	
		question = 'This is a test question'
		question_type = 'Multiple Choice'
		options = ['first option', 'second option']
		display = 'True'
		self.testbed.init_datastore_v3_stub()
		params = {'question': question, 'question_type': question_type, 'options': options, 'display': display}
		# Then pass those values to the handler.
		response = self.testapp.post('/addquestions/', params)
		# Finally verify that the passed-in values are actually stored.
		self.assertEqual(response.status_int, 302)