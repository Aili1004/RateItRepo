#!/usr/bin/env python
#
import datetime
from google.appengine.ext import ndb
from google.appengine.api import users
from models.gtfs import TripsHeadsigns


class RateItUser(ndb.Model):
    user = ndb.UserProperty(required=True)
    user_type = ndb.StringProperty()

    user_sex = ndb.StringProperty(required=True,
                           choices=set(["male", "female"]))
    user_born_year = ndb.StringProperty(required=True)
    user_household_type = ndb.StringProperty(required=True)
    user_postcode = ndb.StringProperty(required=True)
    user_education = ndb.StringProperty(required=True)
    user_occupation = ndb.StringProperty(required=True)
    user_monthly_income = ndb.StringProperty(required=True)
    user_mobility_impairment = ndb.StringProperty(required=True)
    user_device = ndb.StringProperty(required=True)
    user_driver_licence = ndb.StringProperty(required=True)
    user_often_use = ndb.StringProperty(required=True)
    user_purpose_use = ndb.StringProperty(required=True)

    time_registered = ndb.DateTimeProperty(required=True, auto_now_add=True)
    user_selected_bus = ndb.StructuredProperty(TripsHeadsigns)

    # user_often_use = ndb.StringProperty()
    # # proportion of travel using public transport
    # user_proportion_work = ndb.IntegerProperty()
    # user_proportion_education = ndb.IntegerProperty()
    # user_proportion_workrelate = ndb.IntegerProperty()
    # user_proportion_social = ndb.IntegerProperty()
    # user_proportion_shopping = ndb.IntegerProperty()
    # user_proportion_other = ndb.IntegerProperty()
    # # satisfaction with the public transport service in the area you live
    # user_satisfaction_public = ndb.StringProperty()
    # # satisfaction with Forest bus services
    # use_satisfaction_Forest = ndb.StringProperty()
    #
    #
    # # """user_type: Paseenger, Operator, Researcher. """
    #
    # time_registered = ndb.DateTimeProperty(required=True, auto_now_add=True)
    # # time_logged_in = ndb.DateTimeProperty(required=True, auto_now_add=True)
    # # time_logged_out = ndb.DateTimeProperty(required=True, auto_now_add=True)
