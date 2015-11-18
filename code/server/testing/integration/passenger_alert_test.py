# This file tests:
# 1. Whether the PassengerAlert entity has been added to Data Store or not.
# 2. Assume we have '888' as default route_id, it tests whether it has been displayed correctly or not (optional). 
# 3. The maximum length of comment that user can insert. Throws an exception if it exceeds the limit.

# To run it, use the same process as Kevin's integration tests which is in BB.

import unittest
from google.appengine.api import memcache
from google.appengine.ext import ndb
from google.appengine.ext import testbed

class TestModel(ndb.Model):
	route_id = ndb.StringProperty(default="888")
	incident_type = ndb.StringProperty()
	incident_level = ndb.StringProperty()   
	incident_bus_stop = ndb.StringProperty()
	time_of_incident_happened = ndb.StringProperty()
	comment = ndb.StringProperty()

	
class TestEntityGroupRoot(ndb.Model):
	pass

	
def GetEntityViaMemcache(entity_key):
	# Get entity from memcache if available, from datastore if not. 
	entity = memcache.get(entity_key)
	
	if entity is not None:
		return entity
	
	entity = TestModel.get(entity_key)
	
	if entity is not None:
		memcache.set(entity_key, entity)
		
	return entity

	
class DomoTestCase(unittest.TestCase):

	def setUp(self):
		#First, create an instance of the Testbed class.
		self.testbed = testbed.Testbed()
		
		#Then activate the testbed, which prepares the service stubs for 
		self.testbed.activate()
		
		#Next declare which service stubs you want to use.
		self.testbed.init_datastore_v3_stub()
		self.testbed.init_memcache_stub()
	
	#method that deavtivates the bestbed
	def tearDown(self):
		self.testbed.deactivate()
	
	#implement the tests
	def testInsertEntity(self):
		TestModel.put()
		self.assertEqual(1, len(TestModel.all().fetch(2)))
	
	
	# the following is used to check default value for route_id e.g. 888
	# ignore this if we don't need any default values
	def testDefaultRouteId(self):
		root = TestEntityGroupRoot(key_name="root")
		TestModel(parent=root.key()).put()
		TestModel(route_id="777", parent=root.key()).put()
		query = TestModel.all().ancestor(root.key()).filter('route_id =', "888")
		results = query.fetch(2)
		self.assertEqual(1, len(results))
		self.assertEqual("888", results[0].route_id)
	
	
	# testing the maximum length of comment the user inserts (assume the maximum length is 30)
	def testCommentLength(self):
		comment_length = len(TestModel.comment)
		self.assertEqual(30, comment_length)
		self.assertRaises(OutOfRangeError, comment_length, 31)
		
if __name__ == "__main__":
	unittest.main()