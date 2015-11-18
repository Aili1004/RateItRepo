#!/usr/bin/env python

import webapp2
from google.appengine.api import users
from models.rateit_users import RateItUser
from google.appengine.ext import ndb


def register_required():
    find_user = RateItUser.query(RateItUser.user == current_user())
    if find_user.count()<1:
        return True
    else:
        return False

previous_page = ""
def set_pre_page(page):
    global previous_page
    previous_page = page

def get_pre_page():
    return  previous_page

def current_user():
    return users.get_current_user()

def logging_link():
    return (' %s! (<a href="%s">sign out</a>)' %
                        (current_user().email(), users.create_logout_url('/')))

def return_query_count():
    find_user = RateItUser.query(RateItUser.user==users.get_current_user())
    return find_user.count()

def is_registered():
    find_user = RateItUser.query(RateItUser.user==users.get_current_user())
    if find_user.count()>0:
        return True
    else:
        return False

def current_bus():
    find_user = RateItUser.query(RateItUser.user==users.get_current_user())
    if find_user.count() == 1:
	    return find_user.fetch(1)[0].user_selected_bus
		
def change_bus(bus):
    find_user = RateItUser.query(RateItUser.user==users.get_current_user())
    if find_user.count() == 1:
        find_user.fetch(1)[0].user_selected_bus = bus
        find_user.fetch(1)[0].put()
		
		
app = webapp2.WSGIApplication([
    webapp2.Route('/', 'pages.home.home'),
	webapp2.Route('/about', 'pages.about.about'),
	webapp2.Route('/ratetrip', 'pages.ratetrip.ratetrip'),
	webapp2.Route('/alertincident', 'pages.alertincident.alertincident'),
	webapp2.Route('/registration', 'pages.registration.registration'),
	
], debug=True)
# Remove the debug=True parameter above from final version.
