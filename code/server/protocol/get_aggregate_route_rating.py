#!/usr/bin/env python
#

# RPC messages for retrieving aggregate route rating.

from google.appengine.api import memcache
import endpoints
from protorpc import messages
from protorpc import message_types
import logging

import proto_types
import proto_utils
import models.route_rating

LOGGER = logging.getLogger('get_aggregate_route_rating')


class Request(messages.Message):
    """Aggregate route rating requests."""
    # The route number. Either routeId or stopId or both may be specified.
    route_id = messages.StringField(1) 


class AggregateRouteRatingMessage(messages.Message):
    """Message variant of the AggregateRouteRating record."""
    route_id = messages.StringField(1)
    time_of_aggregate_result = message_types.DateTimeField(2, required=True)
    cleanliness = messages.IntegerField(
        3, variant=messages.Variant.INT32, required=True)
    lateness = messages.IntegerField(
        4, variant=messages.Variant.INT32, required=True)
    crowdedness = messages.IntegerField(
        5, variant=messages.Variant.INT32, required=True)

# Convert datastore record to rpc message.
def fromRecord(record):
    return AggregateRouteRatingMessage(
        route_id=record.route_id,
        time_of_aggregate_result=record.time_of_aggregate_result,
        cleanliness=record.cleanliness,
        lateness=record.lateness,
        crowdedness=record.crowdedness
        )

class Response(messages.Message):
    """The response to aggregate route rating requests."""
    # Indicates the success state of the message.
    is_success = messages.BooleanField(1, required=True)
    # The status - available only if success is False.
    status_message = messages.StringField(2, required=False)
    # The rating record - available only if success is True.
    aggregate_route_rating = messages.MessageField(
        AggregateRouteRatingMessage, 3, required=False)


def execute(service, request):
    LOGGER.info('get_aggregate_route_rating.execute() called.')

    route_id = request.route_id

    # See if we have a cached result.
    cacheKey = proto_utils.make_memcache_key(request, route_id)
    response = memcache.get(cacheKey)
    if response:
        return response

    LOGGER.info('Cache missed, performing query.')

    query = models.route_rating.AggregateRouteRating.gql(
        "WHERE route_id = :1 ORDER BY time_of_aggregate_result DESC LIMIT 1", 
        route_id)
    record = query.get()
    if record:
        response = Response(
            is_success=True,
            aggregate_route_rating=fromRecord(record)
            )
    else:
        response = Response(
            is_success=False, 
            status_message="Aggregate rating for route id '%s' not found" % route_id
            )

    # Cache the result so we can avoid a datastore query.
    memcache.set(cacheKey, response, time=proto_utils.CACHE_TIME)
    return response

    


