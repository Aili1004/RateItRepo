import datetime
from google.appengine.ext import ndb
from google.appengine.api import users

import field_types

class Alert(ndb.Model):
  title = ndb.StringProperty(required=True)
  message = ndb.StringProperty(required=True)
  """
  time_start = ndb.DateTimeProperty(required=True, 
							auto_now_add=True)
  time_duration = ndb.DateTimeProperty(required=True)
  """
  type = ndb.StringProperty(required=True,
                           choices=set(["Bus", "Route", "Regional"]))
  priority = ndb.BooleanProperty(required=True)
