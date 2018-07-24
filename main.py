import webapp2
import os
import jinja2
import login




app = webapp2.WSGIApplication([
  ('/', MainHandler),
  ('/login', LoginHandler),
], debug=True)
