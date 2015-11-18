import webapp2
import os
import jinja2
from models.newsfeed_table import Alert
from models.gtfs import TripsHeadsigns
import main
from urlparse import urlparse

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class home(webapp2.RequestHandler):
    def get(self):
        # For endpoints to work, https must be used.  Redirect to https
        # if not running on localhost.
        # parsed = urlparse(self.request.url)
        # if parsed.scheme == 'http' and parsed.hostname != 'localhost':
            # # Redirect to https.
            # self.redirect("https" + self.request.url[4:])
            # return

        page_title = "Home"
        entities = Alert.query().order(Alert.title)
        current_bus = main.current_bus()
        template_values = {
			'page_title': page_title,
            'entities' : entities,
            'headsigns' : TripsHeadsigns.find(),
			'current_bus': current_bus
		}

        template = JINJA_ENVIRONMENT.get_template('templates/home.html')
	self.response.write(template.render(template_values))
	
    def post(self):
        if self.request.get('submit_bus') == "1":
            bus_id = self.request.get('selectbus')
            #self.response.write(bus_id)
            parent = TripsHeadsigns.query().fetch(1)[0].key.parent()
            #self.response.write(parent)
            bus = TripsHeadsigns.get_by_id(bus_id, parent=parent)
            #self.response.write(bus)
            main.change_bus(bus)
            home.get(self)
