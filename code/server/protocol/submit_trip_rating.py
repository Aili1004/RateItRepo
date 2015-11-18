#!/usr/bin/env python
#

# RPC messages for submitting trip rating.

from google.appengine.api import memcache
from google.appengine.api import users
import endpoints
from protorpc import messages
from protorpc import message_types
import logging

import proto_types
import proto_utils
import models.passenger_trip_rating

LOGGER = logging.getLogger('submit_trip_rating')


class Request(messages.Message):
    """Trip rating requests."""
    # The route number. Either routeId or stopId or both may be specified.
    route_id = messages.StringField(1, required=True) 
    is_service_ontime = messages.BooleanField(2, required=True)
    is_service_clean = messages.BooleanField(3, required=True)
    crowdedness =  messages.IntegerField(
        4, variant=messages.Variant.INT32, required=True)
    comfort_rating = messages.IntegerField(
        5, variant=messages.Variant.INT32, required=True)
    driver_rating = messages.IntegerField(
        6, variant=messages.Variant.INT32, required=True)
    comments = messages.StringField(7)


def convert_bool_rating(value):
    if value:
        return 5
    return 1


# Convert request to datastore message.
def convert_request_to_passenger_trip_rating(request, user_id):
    return models.passenger_trip_rating.PassengerTripRating(
        route_id=request.route_id,
        lateness=convert_bool_rating(request.is_service_ontime),
        cleanliness=convert_bool_rating(request.is_service_clean),
        crowdedness=request.crowdedness,
        comfort_level=request.comfort_rating,
        driver_quality=request.driver_rating,
        comment=request.comments,
        user_id=user_id
        )


class Response(messages.Message):
    """The response to submit rating requests."""
    # Indicates the success state of the message.
    is_success = messages.BooleanField(1, required=True)
    # The status - available only if success is False.
    status_message = messages.StringField(2, required=False)


def execute(service, request):
    return execute_with_user(service, request, endpoints.get_current_user())

def execute_with_user(service, request, user_id):
    LOGGER.info('submit_trip_rating.execute() called.')

    route_id = request.route_id

    if not proto_utils.is_route_id_valid(route_id):
        return Response(
            is_success=False, 
            status_message="Route id '%s' not found" % route_id
            )
    
    convert_request_to_passenger_trip_rating(request, user_id).put()
    
    return Response(is_success=True)
    
