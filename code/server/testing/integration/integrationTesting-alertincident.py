from google.appengine.api import memcache
from google.appengine.ext import testbed
import webapp2
import webtest
from models.passenger_alert import PassengerAlert

class AlertIncidentHandler(webapp2.RequestHandler):
	def post(self):
		alertincident = PassengerAlert()
		alertincident.route_id = self.request.get('alertInputRouteId')
		alertincident.incident_type = self.request.get('alertIncidentType')
		alertincident.incident_level = self.request.get('alertInputIncidentLevel')
		alertincident.comment = self.request.get('alertInputComments')
		alertincident.time_of_incident_happened = self.request.get('alertIncidentHappeningTime')
		alertincident.incident_bus_stop = self.request.get('alertInputBusStop')
		
		memcache.set(alertincident.route_id, alertincident.incident_type)
		memcache.set(alertincident.route_id, alertincident.incident_level)
		memcache.set(alertincident.route_id, alertincident.comment)
		memcache.set(alertincident.route_id, alertincident.time_of_incident_happened)
		memcache.set(alertincident.route_id, alertincident.incident_bus_stop)
		
		
class AppTest(unittest.TestCase):
	def setup(self):
		app = webapp2.WSGIApplication([('/', AlertIncidentHandler)])
		self.testapp = webtest.TestApp(app)
		self.testbed = testbed.Testbed()
		self.testbed.activate()
	
	def tearDown(self):
		self.testbed.deactivate()
		
	def testAlertIncidentHandler(self):
		alertincident.route_id = '888'
		alertincident.incident_type = 'Traffic Incident'
		alertincident.incident_level = 'High'
		alertincident.comment = 'No Comment'
		alertincident.time_of_incident_happened = 'Last 10 minutes'
		alertincident.incident_bus_stop = 'university of Sydney'
		
		self.testbed.init_memchache_stub()
		params = {'alertincident.route_id': alertincident.route_id,
				'alertincident.incident_type': alertincident.incident_type,
				'alertincident.incident_level': alertincident.incident_level,
				'alertincident.comment': alertincident.comment,
				'alertincident.time_of_incident_happened': alertincident.time_of_incident_happened,
				'alertincident.incident_bus_stop': alertincident.incident_bus_stop}
		
		response = self.testapp.post('/', params)
		self.assertEquals(alertincident.incident_type, memcache.get(alertincident.route_id))
		self.assertEquals(alertincident.incident_level, memcache.get(alertincident.route_id))
		self.assertEquals(alertincident.comment, memcache.get(alertincident.route_id))
		self.assertEquals(alertincident.time_of_incident_happened, memcache.get(alertincident.route_id))
		self.assertEquals(alertincident.incident_bus_stop, memcache.get(alertincident.route_id))
		
		
		