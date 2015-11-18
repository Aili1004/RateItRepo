import webapp2
import os
import jinja2
#import protocol.submit_trip_rating
import main
from models.passenger_trip_rating import PassengerTripRating
from models.ratetripquestions import Questions


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class ratetrip(webapp2.RequestHandler):
    def get(self):
        main.set_pre_page("ratetrip")
        if main.register_required():
            self.redirect('registration')

        page_title = "Rate Trip"
        entities = Questions.query(Questions.display == True)

        cleanliness = entities.filter(Questions.topic == "Cleanliness")
        comfort = entities.filter(Questions.topic == 'Comfort')
        contribution_to_journey = entities.filter(Questions.topic == 'Contribution to Journey')
        crowding = entities.filter(Questions.topic == 'Crowding')
        customer_service = entities.filter(Questions.topic == 'Customer Service')
        safety_and_security = entities.filter(Questions.topic == 'Safety and Security')
        timeliness = entities.filter(Questions.topic == 'Timeliness')

        template_values = {
            'page_title': page_title,
            'cleanliness': cleanliness,
            'comfort': comfort,
            'contribution_to_journey': contribution_to_journey,
            'crowding': crowding,
            'customer_service': customer_service,
            'safety_and_security': safety_and_security,
            'timeliness': timeliness,
        }

        template = JINJA_ENVIRONMENT.get_template('templates/ratetrip.html')
        self.response.write(template.render(template_values))

    def post(self):
        """
        # Use the endpoints code since the request is validated there.
        request = protocol.submit_trip_rating.Request(
            route_id = self.request.get('inputRouteId3'),
            is_service_ontime = self.request.get('inputServiceOnTime3') == 'T',
            is_service_clean = self.request.get('inputServiceClean3') == 'T',
            crowdedness = int(self.request.get('inputServiceCrowded3')),
            comfort_rating = int(self.request.get('inputServiceComfort3')),
            driver_rating = int(self.request.get('inputDriverPoliteness3')),
            comments = self.request.get('inputComments3')
        )

        response = protocol.submit_trip_rating.execute_with_user(None, request, user_id=None)
        """
        entity = PassengerTripRating()
        entity.route_id = self.request.get('inputRouteId3')
        if(self.request.get_all('Cleanliness') != ''):
            entity.cleanliness = [int(x) for x in self.request.get_all('Cleanliness')]
        if(self.request.get_all('Comfort') != ''):
            entity.comfort = [int(x) for x in self.request.get_all('Comfort')]
        if(self.request.get_all('Contribution to Journey') != ''):
            entity.contribution_to_journey = [int(x) for x in self.request.get_all('Contribution to Journey')]
        if(self.request.get_all('Crowding') != ''):
            entity.crowding = [int(x) for x in self.request.get_all('Crowing')]
        if(self.request.get_all('Customer Service') != ''):
            entity.customer_service = [int(x) for x in self.request.get_all('Customer Service')]
        if(self.request.get_all('Safety and Security') != ''):
            entity.safety_and_security = [int(x) for x in self.request.get_all('Safety and Security')]
        if(self.request.get_all('Timeliness') != ''):
            entity.timeliness = [int(x) for x in self.request.get_all('Timeliness')]
        entity.comment = self.request.get('inputComments3')
        entity.put()

        page_title = "Thank You"

        template_values = {
            'page_title': page_title,
        }

        template = JINJA_ENVIRONMENT.get_template('templates/rateresponse.html')
        self.response.write(template.render(template_values))