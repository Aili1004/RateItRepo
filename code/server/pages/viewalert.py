import webapp2
import os
import jinja2
from operator_handler import OperatorHandler
from models.passenger_alert import PassengerAlert

JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions=['jinja2.ext.autoescape'],
	autoescape=True)

class viewalert(OperatorHandler):
	def get(self):
		page_title = "View Alerts"
		
		#retrieve values from the datastore
		entities_query = PassengerAlert.query()
		entities = entities_query.fetch(10)
		
		template_values = {
			'page_title': page_title,
            'extends_template' : self.get_template(),
			'entities': entities,
		}
		
		template = JINJA_ENVIRONMENT.get_template('templates/viewalert.html')
		self.response.write(template.render(template_values))
		