#!/usr/bin/env python
#

# RPC messages for submitting incident

from google.appengine.api import memcache
from google.appengine.api import users
import endpoints
from protorpc import messages
from protorpc import message_types
import logging
import endpoints
import proto_types
import proto_utils
import models.passenger_alert

LOGGER = logging.getLogger('submit_incident')


class Request(messages.Message):
    """incident alerting requests."""
    # The route number. Either routeId or stopId or both may be specified.
    route_id = messages.StringField(1, required=True) 
    incident_type = messages.StringField(2, required=True)
    incident_level = messages.StringField(3, required=True)    
    comments = messages.StringField(4)
    time_of_incident_happened = messages.StringField(5, required=True)
    incident_bus_stop = messages.StringField(6, required=True)

# Convert request to datastore message.
def convert_request_to_passenger_create_alert(request):
    return models.passenger_alert.PassengerAlert(
        route_id=request.route_id,
        incident_type=request.incident_type,
        incident_level=request.incident_level,
        comments=request.comments,
        incident_bus_stop = request.incident_bus_stop,
        time_of_incident_happened = request.time_of_incident_happened,
        user_id=users.get_current_user()
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
    LOGGER.info('submit_incident.execute() called.')

    route_id = request.route_id

    if not proto_utils.is_route_id_valid(route_id):
        return Response(
            is_success=False, 
            status_message="Route id '%s' not found" % route_id
            )
    
    convert_request_to_passenger_trip_rating(request, user_id).put()
    
    return Response(is_success=True)
	