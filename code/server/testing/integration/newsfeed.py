import datetime
from google.appengine.ext import db
from google.appengine.api import users


class Alert(db.Model):
  message = db.StringProperty(required=True)
  type = db.StringProperty(required=True,
                           choices=set(["Bus", "Route", "Regional"]))
  priority = db.StringProperty(required=True,
                           choices=set(["Low", "Med", "High"]))
  pushed = db.BooleanProperty(indexed=False)

