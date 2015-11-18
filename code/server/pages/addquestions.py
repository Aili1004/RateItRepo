import webapp2
import os
import jinja2
from models.ratetripquestions import Questions
from operator_handler import ResearcherHandler


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class addquestions(ResearcherHandler):
	def get(self):
		page_title = "Add Questions (Rate Trip)"
		
		template_values = {
			'page_title': page_title,
			'extends_template' : self.get_template(),
		}
		
		template = JINJA_ENVIRONMENT.get_template('templates/addquestions.html')
		self.response.write(template.render(template_values))
		
	def post(self):
		question = Questions()
		question.question = self.request.get('question')
		question.question_type = self.request.get('response type')
		question.options = self.request.get_all('option')
		question.name = self.request.get('name')
		question.topic = self.request.get('topic')
		question.display = False
		question.put()
		
		self.redirect('/researcher/addquestions')