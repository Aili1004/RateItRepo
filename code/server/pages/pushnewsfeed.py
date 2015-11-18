import webapp2
import os
import jinja2
import logging
from operator_handler import OperatorHandler
import google.appengine.ext.db
from models.newsfeed_table import Alert
import main

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
"""	
class BaseHandler(OperatorHandler):
    def handle_exception(self, exception, debug):
        # Log the error.
        logging.exception(exception)

        # Set a custom message.
        ERROR_MESSAGE = \"""
			<script>
				alert("An error has occurred.");
			</script>
		\"""
        #self.response.write(exception)
        if isinstance(exception, google.appengine.ext.db.BadValueError):
			pushnewsfeed.get(self)
			self.response.write('<h3 style="color: Red; padding-left:100"><b>Please fill out the form correctly.</b></h3>')
			\""" 
			self.response.write(exception)
			self.response.write(ERROR_MESSAGE)
			\"""
        else:
			self.response.write(ERROR_MESSAGE)
"""

#class pushnewsfeed(BaseHandler):
class pushnewsfeed(OperatorHandler):
    def get(self):

        page_title = "Push Newsfeed"
        entities = Alert.query().order(Alert.title)
		
        template_values = self.make_template_dict(
			page_title=page_title,
            entities=entities)

        template = JINJA_ENVIRONMENT.get_template('templates/pushnewsfeed.html')
        self.response.write(template.render(template_values))		
		
    def post(self):
        if self.request.get('create_newsfeed_form_submit') == "1":
			newsfeed = Alert()
			newsfeed.title = self.request.get('alertTitle')
			newsfeed.message = self.request.get('alertMessage')
			newsfeed.type = self.request.get('alertType')
			#newsfeed.time_start = self.request.get('alertStartTime')
			#newsfeed.time_duration = self.request.get('alertDuration')
			if self.request.get('alertPriority') == 'True':
				newsfeed.priority = True
			else:
				newsfeed.priority = False
			newsfeed.put()
        elif self.request.get('submit_changes') == "1":
			#This can be done better but it works for now
			entities = Alert.query().order(Alert.title)
			for a in entities:
				id = a.key.integer_id()
				if self.request.get('%d' % (id)) == "1":
					a.priority = True
					a.put()
				elif self.request.get('%d' % (id)) == "2":
					a.priority = False
					a.put()
				elif self.request.get('%d' % (id)) == "3":
					a.key.delete()
			
        self.redirect(self.get_submit_path())
        
    def get_submit_function_name(self):
        return 'pushnewsfeed'
