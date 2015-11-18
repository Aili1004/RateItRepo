import webapp2
import os
import jinja2
import logging
import google.appengine.ext.db
import webtest
from pages.registration import registration
import unittest
from google.appengine.ext import testbed

class AppTest(unittest.TestCase):

    def setUp(self):
        # Create a WSGI application.
        app = webapp2.WSGIApplication([('/registration/', registration)])
        # Wrap the app with WebTest’s TestApp.
        self.testapp = webtest.TestApp(app)
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()


    def tearDown(self):
        self.testbed.deactivate()

    def testRegistrationHandler(self):
        res = self.testapp.get('/registration')
        self.assertEqual(res.status_int, 200)

        # First define a key and value to be cached.
        sex = 'sex'
        inputYear = 'inputYear'
        householdType = 'householdType'
        postcode = 'postcode'
        education = 'education'
        occupation = 'occupation'
        monthly_income = 'monthly_income'
        mobility_impairment = 'mobility_impairment'
        often_use = 'often_use'
        devices_type = 'devices_type'
        drivers_licence = 'drivers_licence'
        purpose_to_use = 'purpose_to_use'
        self.testbed.init_datastore_v3_stub()
        params = {
            'sex': sex,
            'inputYear': inputYear,
            'householdType': householdType,
            'postcode': postcode,
            'education': education,
            'occupation': occupation,
            'monthly_income': monthly_income,
            'mobility_impairment': mobility_impairment,
            'often_use': often_use,
            'devices_type': devices_type,
            'drivers_licence': drivers_licence,
            'purpose_to_use': purpose_to_use
        }
        # Then pass those values to the handler.
        response = self.testapp.post('/registration/', params)
        # Finally verify that the passed-in values are actually stored.
        self.assertEqual(response.status_int, 302)
