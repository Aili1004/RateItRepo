import unittest
from google.appengine.api import memcache
from google.appengine.ext import ndb
from google.appengine.ext import testbed
from google.appengine.api import users

from models.rateit_users import RateItUser
from pages.registration import registration
import main

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

    # The following are testing data model RateItUser
    def testInsertEntity(self):
        RateItUser().put()
        self.assertEqual(1, len(RateItUser.all().fetch(2)))

    def test_empty_input(self):
        mytest = RateItUser()
        result = mytest.put()
        self.assertEqual(None, ndb.get(result).user)
        self.assertEqual(None, ndb.get(result).user_type)
        self.assertEqual(None, ndb.get(result).user_sex)
        self.assertEqual(None, ndb.get(result).user_born_year)
        self.assertEqual(None, ndb.get(result).user_household_type)
        self.assertEqual(None, ndb.get(result).user_postcode)
        self.assertEqual(None, ndb.get(result).user_education)
        self.assertEqual(None, ndb.get(result).user_occupation)
        self.assertEqual(None, ndb.get(result).user_monthly_income)
        self.assertEqual(None, ndb.get(result).user_mobility_impairment)
        self.assertEqual(None, ndb.get(result).user_device)
        self.assertEqual(None, ndb.get(result).user_driver_licence)
        self.assertEqual(None, ndb.get(result).user_often_use)
        self.assertEqual(None, ndb.get(result).user_purpose_use)

    def test_insert_user(self):
        mytest = RateItUser(user=users.get_current_user())
        result = mytest.put()
        self.assertEqual(users.get_current_user(), ndb.get(result).user)

    def test_insert_user_type(self):
        mytest = RateItUser(user_type='passenger')
        result = mytest.put()
        self.assertEqual('passenger', ndb.get(result).user_type)

    def test_insert_user_sex(self):
        mytest = RateItUser(user_sex='Male')
        result = mytest.put()
        self.assertEqual('male', ndb.get(result).user_sex)
        mytest1 = RateItUser(user_sex = 'female')
        result1 = mytest1.put()
        self.assertEqual('female', ndb.get(result1).user_sex)
        # entered text neither 'male'('Male') or 'female'('Female')
        mytest2 = RateItUser(user_sex='other')
        result2 = mytest2.put()
        self.assertEqual(None, ndb.get(result2).user_sex)

    def test_insert_born_year(self):
        mytest = RateItUser(user_born_year='1990')
        result = mytest.put()
        self.assertEqual('1990', ndb.get(result).user_born_year)

    def test_insert_user_household_type(self):
        mytest = RateItUser(user_household_type='household')
        result = mytest.put()
        self.assertEqual('household', ndb.get(result).user_household_type)

    def test_insert_user_postcode(self):
        mytest = RateItUser(user_postcode='2000')
        result = mytest.put()
        self.assertEqual('2000', ndb.get(result).user_postcode)

    def test_insert_user_education(self):
        mytest = RateItUser(user_education='education')
        result = mytest.put()
        self.assertEqual('education', ndb.get(result).user_education)

    def test_insert_user_occupation(self):
        mytest = RateItUser(user_occupation='occupation')
        result = mytest.put()
        self.assertEqual('occupation', ndb.get(result).user_occupation)

    def test_insert_user_monthly_income(self):
        mytest = RateItUser(user_monthly_income='monthly income')
        result = mytest.put()
        self.assertEqual('monthly income', ndb.get(result).user_monthly_income)

    def test_insert_user_mobility_impairment(self):
        mytest = RateItUser(user_mobility_impairment='mobility impairment')
        result = mytest.put()
        self.assertEqual('mobility impairment', ndb.get(result).user_mobility_impairment)

    def test_insert_user_device(self):
        mytest = RateItUser(user_device='device')
        result = mytest.put()
        self.assertEqual('device', ndb.get(result).user_device)

    def test_insert_user_driver_licence(self):
        mytest = RateItUser(user_driver_licence='drivers licence')
        result = mytest.put()
        self.assertEqual('drivers licence', ndb.get(result).user_driver_licence)

    def test_insert_user_often_use(self):
        mytest = RateItUser(user_often_use='often use')
        result = mytest.put()
        self.assertEqual('often use', ndb.get(result).user_often_use)

    def test_insert_user_purpose_use(self):
        mytest = RateItUser(user_purpose_use='purpose use')
        result = mytest.put()
        self.assertEqual('purpose use', ndb.get(result).user_purpose_use)

    def test_insert_device(self):
        mytest = RateItUser()
        result = mytest.put()
        self.assertEqual(None, ndb.get(result).user_device)

        mytest1 = RateItUser(user_device='iPhone')
        result1 = mytest1.put()
        self.assertEqual('iPhone', ndb.get(result1).user_device)


#     The following are testing helper functions
    def test_set_pre_page(self):
        page = 'homepage'
        self.assertEqual('homepage',main.set_pre_page(page))


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()