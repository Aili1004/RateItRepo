#!/usr/bin/env python
#

# This is a template for RPC requests to the server using App Engine endpoints.
# Every RPC will have a Request and Response classes that respectively
# encapsulate the request and response messages.
#

import endpoints
from protorpc import messages
from protorpc import message_types
import logging

import proto_types

LOGGER = logging.getLogger('issue_report')


class ExampleError(Exception):
    pass

class Request(messages.Message):
    """Issue report requests."""
    # The route number. Either routeId or stopId or both may be specified.
    route_id = messages.StringField(1) 
    
    # The stop id.
    stop_id = messages.StringField(2)

    # The browser timestamp for this message.
    report_date_time = message_types.DateTimeField(3, required=True)
    
    # The type of rating, e.g. crowding, cleanliness tardiness etc.
    rating_type = messages.EnumField(proto_types.IssueType, 4, required=True)
    
    gps_location = messages.MessageField(
        proto_types.GPSLocation, 5, required=False)


class Response(messages.Message):
    """The response to issue report requests."""
    responseText = messages.StringField(1)


def execute(service, request):
    LOGGER.info('issue_report.execute() called. %s' % str(service.__class__))
    response = Response(responseText = 'This function is not implemented!! Please implement me.')

    testf()

    if request.rating_type == proto_types.IssueType.CROWDED:
        raise ExampleError()
    return response

# This is temporary test code...

import models.test_table
import models.route_rating
import datetime

def testf():

    record = models.test_table.Test(
        s="angela", abc="a", a_date=datetime.datetime.now().date(), tf=True)
    record.put()

    record = models.route_rating.AggregateRouteRating(
        route_id="616X", cleanliness=50, lateness=50, crowdedness=50,
        time_of_aggregate_result=datetime.datetime.now())
    record.put()


