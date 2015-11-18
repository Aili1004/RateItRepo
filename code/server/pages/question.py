import webapp2
import os
import jinja2
from models.ratetripquestions import Questions
from operator_handler import ResearcherHandler

JINJA_ENVIRONMENT = jinja2.Environment(
        loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
        extensions=['jinja2.ext.autoescape'],
        autoescape=True)
		
class question(ResearcherHandler):
    def get(self, id):
        page_title = "View Ratings"
        
        #retrieve values from the datastore
        entity = Questions.get_by_id(long(id))
        
        template_values = self.make_template_dict(
            page_title=page_title,
            entity=entity)
        
        template = JINJA_ENVIRONMENT.get_template('templates/question.html')
        self.response.write(template.render(template_values))
    	
    def post(self, id):
        entity = Questions.get_by_id(long(id))
        if (self.request.get('toggledisplay') == 'true'):
            entity.display = True
        else:
            entity.display = False
        entity.put()
        self.redirect('/' + self.user_interface_name() + '/viewquestions/id=' + id)
        
    def get_submit_function_name(self):
        return 'viewquestions'