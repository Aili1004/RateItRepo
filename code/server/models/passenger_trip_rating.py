import datetime
from google.appengine.ext import ndb
from google.appengine.api import users

import field_types

class PassengerTripRating(ndb.Model):
	"""Table for ratings of trips."""
	"""route_id = field_types.ROUTE_ID()
	lateness = field_types.RATING()
	cleanliness = field_types.RATING()
	crowdedness = field_types.RATING()
	comfort_level = field_types.RATING()
	driver_quality = field_types.RATING()
	comment = ndb.StringProperty(required=False)
	time_of_rating = ndb.DateTimeProperty(auto_now_add=True)
	user_id = ndb.UserProperty()"""
	route_id = ndb.StringProperty(required=True)
	cleanliness = ndb.IntegerProperty(repeated=True)
	comfort = ndb.IntegerProperty(repeated=True)
	contribution_to_journey = ndb.IntegerProperty(repeated=True)
	crowding = ndb.IntegerProperty(repeated=True)
	customer_service = ndb.IntegerProperty(repeated=True)
	safety_and_security = ndb.IntegerProperty(repeated=True)
	timeliness = ndb.IntegerProperty(repeated=True)
	comment = ndb.StringProperty()
	time_of_rating = ndb.DateTimeProperty(auto_now_add=True)