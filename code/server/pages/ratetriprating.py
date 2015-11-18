import webapp2
import os
import jinja2
from models.passenger_trip_rating import PassengerTripRating

JINJA_ENVIRONMENT = jinja2.Environment(
        loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
        extensions=['jinja2.ext.autoescape'],
        autoescape=True)
		
class ratetriprating(webapp2.RequestHandler):
	def get(self, id):
		page_title = "View Ratings"

		#retrieve values from the datastore
		entity = PassengerTripRating.get_by_id(long(id))
		
		template_values = {
			'page_title': page_title,
			'entity' : entity,
		}
		
		template = JINJA_ENVIRONMENT.get_template('templates/ratetriprating.html')
		self.response.write(template.render(template_values))