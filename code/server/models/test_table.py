import datetime
from google.appengine.ext import db
from google.appengine.api import users


class Test(db.Model):
  s = db.StringProperty(required=True)
  abc = db.StringProperty(required=True,
                           choices=set(["a", "b", "c"]))
  a_date = db.DateProperty()
  tf = db.BooleanProperty(indexed=False)


