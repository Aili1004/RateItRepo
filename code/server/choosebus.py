import cgi
import urllib

from google.appengine.api import users
# [START import_ndb]
from google.appengine.ext import ndb

# [END import_ndb]

import webapp2



class Bus(ndb.Model):
    busrouteid = ndb.StringProperty()
    busstopname = ndb.StringProperty()

class ChooseBus(webapp2.RequestHandler):
    def get(self):
        self.response.write('<html><head>')
        self.response.write("Add Bus and Stops")
        AddBusForm = """
        <form method="get">
        Bus Route ID:
        <div><input type="text" name="busrouteid" /></div>
        Bus Stops:
        <div><input type="text" name="busstopname" /></div>
        <div><input type="submit" value="Add Bus"></div>
		</form>
        """
        self.response.write(AddBusForm)
        # Get information from form
        form = cgi.FieldStorage()
        aBus = Bus()
        aBus.busrouteid = form.getvalue('busrouteid')
        aBus.busstopname = form.getvalue('busstopname')
        # Store information into datastore
        aBus.put()
        
        # Query from datastore and dispaly them in a drop down list "Choose a bus"
        buses = Bus.query(projection=["busrouteid", "busstopname"], distinct=True).order(Bus.busrouteid)
        self.response.write("""<form method="get"> """)
        self.response.write("Choose a bus:")
        self.response.write("""<select name="busrouteDrop">""")
        for bus in buses:
            self.response.write("""<option value="%s"> %s </option>""" % (bus.busrouteid,bus.busrouteid))
        self.response.write("</select><br>")
        # Joined at a bus stop
        self.response.write("I joined at:")
        self.response.write("""<select name="busstopDrop">""")
        for bus in buses:
            self.response.write("""<option value="%s"> %s </option>""" % (bus.busstopname,bus.busstopname))
        self.response.write("</select><br>")
        # Going to a bus stop
        self.response.write("I am going to:")
        self.response.write("""<select name="busstopDrop">""")
        for bus in buses:
            self.response.write("""<option value="%s"> %s </option>""" % (bus.busstopname,bus.busstopname))
        self.response.write("</select><br>")
        
        self.response.write("</form>")
    
        self.response.write('</body></html>')

application = webapp2.WSGIApplication([
    ('/', ChooseBus),
], debug=True)
