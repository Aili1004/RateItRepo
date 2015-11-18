import webapp2
import os
import jinja2
from models.ratetripquestions import Questions
from operator_handler import ResearcherHandler


JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions=['jinja2.ext.autoescape'],
	autoescape=True)
	
class viewquestions(ResearcherHandler):
	def get(self):

		entities = Questions.query()
		
		page_title = "View Questions (Rate Trip)"
		
		template_values = {
			'page_title': page_title,
			'entities': entities,
			'extends_template' : self.get_template(),
		}
		
		template = JINJA_ENVIRONMENT.get_template('templates/viewquestions.html')
		self.response.write(template.render(template_values))
