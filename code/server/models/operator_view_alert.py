import datetime
from google.appengine.ext import ndb
from google.appengine.api import users

#import field_types

class OperatorViewAlert(ndb.Model):
	route_id = ndb.StringProperty()
	incident_type = ndb.StringProperty()
	incident_level = ndb.StringProperty()
	comment = ndb.StringProperty()
	time_of_reporting_incident = ndb.DateTimeProperty(auto_now_add=True)