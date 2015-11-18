from google.appengine.ext import ndb

import field_types

class Questions(ndb.Model):
	question = ndb.StringProperty(required=True)
	question_type = ndb.StringProperty(required=True)
	options = ndb.StringProperty(repeated=True)
	display = ndb.BooleanProperty(required=True)
	name = ndb.StringProperty(required=True)
	topic = ndb.StringProperty(required=True)