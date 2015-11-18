import datetime
from google.appengine.ext import ndb
from google.appengine.api import users

import field_types


class AggregateRouteRating(ndb.Model):
    """Computed table of ratings for various routes."""
    route_id = field_types.ROUTE_ID()
    cleanliness = field_types.RATING()
    lateness = field_types.RATING()
    crowdedness = field_types.RATING()
    time_of_aggregate_result = ndb.DateTimeProperty(auto_now_add=True)
    #TODO(Angela) Add correct rating fields.