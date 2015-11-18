import webapp2
import os
import jinja2

from urlparse import urlparse

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class about(webapp2.RequestHandler):
    def get(self):
		page_title = "About"
		
		template_values = {
			'page_title': page_title,
		}

		template = JINJA_ENVIRONMENT.get_template('templates/about.html')
		self.response.write(template.render(template_values))