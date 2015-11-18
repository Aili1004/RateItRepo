import unittest
from google.appengine.api import memcache
from google.appengine.ext import ndb
from google.appengine.ext import testbed
from models.newsfeed_table import Alert  


class TestEntityGroupRoot(ndb.Model):
    """ Entity group root"""
    pass


def GetEntityViaMemcache(entity_key):
    """ Get entity from memcache if available, from datastore if not. """
    entity = memcache.get(entity_key)
    
    if entity is not None:
        return entity
    
    entity = TestModel.get(entity_key)
    
    if entity is not None:
        memcache.set(entity_key, entity)
        
    return entity


class DemoTestCase(unittest.TestCase):
    
    def setUp(self):
        """First, create an instance of the Testbed class. """
        self.testbed = testbed.Testbed()
        
        """Then activate the testbed, which prepares the service stubs for """
        self.testbed.activate()
        
        """Next declare which service stubs you want to use."""
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()


    """method that deactivates the testbed"""
    def tearDown(self):
        self.testbed.deactivate()
        
        
        
    """ test the title"""
    def testInsertAlertTitle(self):
        mytest = Alert()
        result = mytest.put()
        self.assertEqual(None, ndb.get(result).title)
        
        mytest1 = Alert(title='title')
        result1 = mytest1.put()
        self.assertEqual('title', ndb.get(result1).title)
        
        
    """test the alert type"""
    def testInsertAlertType(self):
        mytest = Alert()
        result = mytest.put()
        self.assertEqual(None, ndb.get(result).type)
        
        mytest1 = Alert(type='Bus')
        result1 = mytest1.put()
        self.assertEqual('Bus', ndb.get(result1).type)
        
        mytest2 = Alert(type='Route')
        result2 = mytest2.put()
        self.assertEqual('Route, ndb.get(result2).type)
        
        mytest3 = Alert(type='Regional')
        result3 = mytest3.put()
        self.assertEqual('Regional', ndb.get(result3).type)
        
    
    """ test the message """
    def testInsertMessage(self):
        mytest = Alert()
        result = mytest.put()
        self.assertEqual(None, ndb.get(result).type)
        
        mytest1 = Alert(message='testing')
        result1 = mytest1.put()
        self.assertEqual('testing', ndb.get(result1).message)
        
        mytest2 = Alert(message='234324')
        result2 = mytest2.put()
        self.assertEqual('234324', ndb.get(result2).message)
        
        mytest3 = Alert(incident_type='fdjgidgjidjgidjgirgjrigjfigjdfgijdfigjdfigjfigjfigjfijgifjgifjgfigj')
        result3 = mytest3.put()
        self.assertEqual('fdjgidgjidjgidjgirgjrigjfigjdfgijdfigjdfigjfigjfigjfijgifjgifjgfigj', ndb.get(result3).message)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()