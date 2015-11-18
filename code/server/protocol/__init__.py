#!/usr/bin/env python
#

import proto_types
import endpoints
import issue_report
import get_aggregate_route_rating
import submit_trip_rating
import submit_passenger_alert

from protorpc import remote

CLIENT_IDS=['314357337812-0569sb35jc4vpq8gqihrlk5kkl3e2bie.apps.googleusercontent.com']


@endpoints.api(name='rateit',version='v1',
               description='RateIt REST API')
class RateItRestApi(remote.Service): 

    @endpoints.method(issue_report.Request,
                      issue_report.Response,
                      name='issue.report')
    def issueReport(self, request):
        return issue_report.execute(self, request)

    @endpoints.method(get_aggregate_route_rating.Request,
                      get_aggregate_route_rating.Response,
                      name='aggregate_route_rating.get')
    def getAggregateRouteRating(self, request):
        return get_aggregate_route_rating.execute(self, request)

    @endpoints.method(submit_trip_rating.Request,
                      submit_trip_rating.Response,
                      name='trip_rating.submit',
                      auth_level=endpoints.AUTH_LEVEL.REQUIRED,
                      allowed_client_ids=CLIENT_IDS)
    def submitTripRating(self, request):
        return submit_trip_rating.execute(self, request)
        
        
    @endpoints.method(submit_passenger_alert.Request,
                      submit_passenger_alert.Response,
                      name='incident_alert.submit')
    
    def submitIncident(self, request):
        return submit_passenger_alert.execute(self, request)
