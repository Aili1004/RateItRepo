#!/usr/bin/env python

import webapp2
import pages.operator_handler

OPERATOR_ROUTES = [
	('/operator', 'pages.viewratings.viewratings'),
	('/operator/', 'pages.viewratings.viewratings'),
	('/operator/viewratings', 'pages.viewratings.viewratings'),
	('/operator/viewalert', 'pages.viewalert.viewalert'),
	('/operator/pushnewsfeed', 'pages.pushnewsfeed.pushnewsfeed'),
	('/operator/viewratings/id=<:\d+>', 'pages.ratetriprating.ratetriprating'),
	('/operator/viewalert/id=<:\d+>', 'pages.viewalertdetails.viewalertdetails'),
]

def make_researcher_path(str):
    return '/researcher' + str[len('/operator'):]

def make_researcher_handler(cls_str):
    cls_path = cls_str.split('.')
    module = __import__('.'.join(cls_path[:-1]))
    for mname in cls_path[1:-1]:
        module = getattr(module, mname)
    cls = getattr(module, cls_path[-1])
    # Makes a derived class using ResearcherOverrides.
    return type('Researcher%s' % cls_path[-1], (pages.operator_handler.ResearcherOverrides, cls), {})

# Researcher interfaces are all the operator interfaces plus some.
RESEARCHER_ROUTES = [ 
    (make_researcher_path(a[0]), make_researcher_handler(a[1])) for a in OPERATOR_ROUTES ] + [
        ('/researcher/upload_gtfs', 'pages.operator_upload_gtfs.operator_upload_gtfs'),
        ('/researcher/user_roles_admin', 'pages.user_roles_admin.user_roles_admin'),
        ('/researcher/viewquestions/id=<:\d+>', 'pages.question.question'),
        ('/researcher/addquestions', 'pages.addquestions.addquestions'),
        ('/researcher/viewquestions', 'pages.viewquestions.viewquestions'),
    ]

operator = webapp2.WSGIApplication(
    [ webapp2.Route(*a) for a in OPERATOR_ROUTES ], debug=True)

researcher = webapp2.WSGIApplication(
    [ webapp2.Route(*a) for a in RESEARCHER_ROUTES ], debug=True)
# Remove the debug=True parameter above from final version.
