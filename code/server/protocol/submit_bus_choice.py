#!/usr/bin/env python
#

# RPC messages for submitting bus choice.

from google.appengine.api import memcache
from google.appengine.api import users
import endpoints
from protorpc import messages
from protorpc import message_types
import logging

import proto_types
import proto_utils
import models.passenger_bus_choice

LOGGER = logging.getLogger('submit_bus_choice')


class Request(messages.Message):
    """Bus choice requests."""
    # The route number. Both of routeId and stopId should be specified.
    route_id = messages.StringField(1, required=True) 
    stop_id_from = messages.StringField(2, required=True)
    stop_id_to = messages.StringField(3, required=True)

# Convert request to datastore message.
def convert_request_to_passenger_bus_choice(request):
    return models.passenger_bus_choice.PassengerBusChoice(
        route_id=request.route_id,
        strop_id_from = request.strop_id_from
        strop_id_to = request.strop_id_to
        )


class Response(messages.Message):
    """The response to submit bus choice requests."""
    # Indicates the success state of the message.
    is_success = messages.BooleanField(1, required=True)
    # The status - available only if success is False.
    status_message = messages.StringField(2, required=False)


def execute(service, request):
    LOGGER.info('submit_bus_choice.execute() called.')

    route_id = request.route_id
    stop_id_from = request.stop_id_from
    stop_id_to = request.stop_id_to
    
    if not proto_utils.is_route_id_valid(route_id):
        return Response(
            is_success=False,
            status_message="Route id '%s' not found" % route_id
            )
    if not proto_utils.is_stop_id_valid(strop_id_from):
        return Response(
               is_success=False,
               status_message="Stop id '%s' not found for 'I joined at' field" % stop_id_from
            )
    if not proto_utils.is_stop_id_valid(strop_id_to):
        return Response(
               is_success=False,
               status_message="Stop id '%s' not found for 'I am going to' field" % stop_id_to
               )
    convert_request_to_passenger_bus_choice(request).put()
    
    return Response(is_success=True)