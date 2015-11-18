import webapp2
import os
import jinja2
from models.passenger_alert import PassengerAlert
import main
from models.gtfs import TripsHeadsigns
from models.gtfs import Stops
from urlparse import urlparse

JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions=['jinja2.ext.autoescape'],
	autoescape=True)


class alertincident(webapp2.RequestHandler):
	def get(self):
		main.set_pre_page("alertincident")
		if main.register_required():
			self.redirect('registration')

		page_title = "Alert Incident"
		

		# retrieve values from the datastore
		entities_query2 = PassengerAlert.query()
		entities2 = entities_query2.fetch(10)

		template_values = {
			'page_title': page_title,
			#'entities2': entities2,
			'headsigns2' : TripsHeadsigns.find(),
			'stops': Stops.find()
		}

		template = JINJA_ENVIRONMENT.get_template('templates/alertincident.html')
		self.response.write(template.render(template_values))


	def post(self):
		alertincident = PassengerAlert()
		alertincident.route_id = self.request.get('alertInputRouteId')
		alertincident.incident_type = self.request.get('alertIncidentType')
		alertincident.incident_level = self.request.get('alertInputIncidentLevel')
		alertincident.comment = self.request.get('alertInputComments')
		alertincident.time_of_incident_happened = self.request.get('alertIncidentHappeningTime')
		alertincident.incident_bus_stop = self.request.get('alertInputBusStop')
		
		alertincident.put()
		
		page_title = "Thank You"

		template_values = {
			'page_title': page_title,
		}

		template = JINJA_ENVIRONMENT.get_template('templates/rateresponse.html')
		self.response.write(template.render(template_values))