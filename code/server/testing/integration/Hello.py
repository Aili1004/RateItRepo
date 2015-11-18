import webapp2
import webtest

class HelloWorldHandler(webapp2.RequestHandler):
   def get(self):
       # Create the handler's response "Hello World!" in plain text.
       self.response.headers['Content-Type'] = 'text/plain'
       self.response.out.write('Hello World!')