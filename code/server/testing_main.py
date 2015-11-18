#!/usr/bin/env python

import webapp2

app = webapp2.WSGIApplication([
    webapp2.Route('/testing', 'testing.RunTests.RunTests'),
    webapp2.Route('/testing/', 'testing.RunTests.RunTests'),
], debug=True)
# Remove the debug=True parameter above from final version.
