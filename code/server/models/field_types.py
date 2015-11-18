import datetime
from google.appengine.ext import ndb
from google.appengine.api import users


def ROUTE_ID(required=True):
  return ndb.StringProperty(required=required)

def RATING(required=True):
  return ndb.IntegerProperty(required=required)

def ALERTING(required=True):
    return ndb.StringProperty(required=required)