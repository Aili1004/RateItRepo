import webapp2
import os
import jinja2
from models.passenger_alert import PassengerAlert
from operator_handler import OperatorHandler

JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions=['jinja2.ext.autoescape'],
	autoescape=True)

class viewalertdetails(OperatorHandler):
	def get(self, id):
		page_title = "View Alert"
		
		entity = PassengerAlert.get_by_id(long(id))
		
		template_values = {
			'page_title': page_title,
			'entity': entity,
			'extends_template' : self.get_template(),
		}
		
		template = JINJA_ENVIRONMENT.get_template('templates/viewalertdetails.html')
		self.response.write(template.render(template_values))
		
	def post(self, id):
		entity = PassengerAlert.get_by_id(long(id))
		#if(self.request.get("onoffswitch") == 'true'):
		#entity.on_off = True
		#else:
			#entity.on_off = False
		
		entity.put()
		self.redirect('/operator/viewalert/id=' + id)
	