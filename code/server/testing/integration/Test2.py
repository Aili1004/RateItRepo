import webapp2
import os
import jinja2
import logging
import google.appengine.ext.db
import webtest
from pages.pushnewsfeed import pushnewsfeed
import unittest
from models.newsfeed_table import Alert
from google.appengine.ext import testbed

class AppTest(unittest.TestCase):

  def setUp(self):
    app = webapp2.WSGIApplication([('/pushnewsfeed/', pushnewsfeed)])
    self.testapp = webtest.TestApp(app)
    self.testbed = testbed.Testbed()
    self.testbed.activate()
    self.testbed.init_datastore_v3_stub()

  def tearDown(self):
     self.testbed.deactivate()

  def testPushNewsfeedHandler(self):
    res = self.testapp.get('/pushnewsfeed/')
    self.assertEqual(res.status_int, 200)
    title = 'Title'
    message = 'blah'
    type = 'Bus'
    priority = 'True'
    self.testbed.init_datastore_v3_stub()
    params = {'title': title, 'message': message, 'type': type, 'priority': priority}
    # Then pass those values to the handler.
    response = self.testapp.post('/pushnewsfeed/', params)
    # Finally verify that the passed-in values are actually stored.
    self.assertEqual(response.status_int, 302)
	
    """
	res = app.get('/pushnewsfeed')
	form = res.forms['create_newsfeed_form']
	form['alertTitle'] = 'Title'
	form['alertMessage'] = 'blah'
	form['alertType'] = 'Bus'
	form['alertPriority'] = 'True'
	res = form.submit('create_newsfeed_form_submit')
	print(res)
	
	"""
