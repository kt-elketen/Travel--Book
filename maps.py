import os
import webapp2
import jinja2
import logging
import time
from google.appengine.ext import ndb

JINJA_ENV = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

<<<<<<< HEAD
#class CoordsRequest(ndb.Model):
#    lat = ndb.StringProperty(required = True)
#    lon = ndb.StringProperty(required = True)
#    timestamp = ndb.DateTimeProperty(auto_now_add = True)
=======
class CoordsRequest(ndb.Model):
    lat = ndb.StringProperty(required = True)
    lon = ndb.StringProperty(required = True)
    timestamp = ndb.DateTimeProperty(auto_now_add = True)
>>>>>>> 35050159178fff696eb967b9356de09cc4dfb777

class AddressRequest(ndb.Model):
    address = ndb.StringProperty(required = True)
    timestamp = ndb.DateTimeProperty(auto_now_add = True)

class RecordRequestHandler(webapp2.RequestHandler):
    def post(self):
        logging.info(self.request)
<<<<<<< HEAD
        if  self.request.get('type') == "address":
=======
        if self.request.get('type') == "coords":
            new_record = CoordsRequest(lat = self.request.get('lat'),
                                       lon = self.request.get('lon'))
            new_record.put()
        elif self.request.get('type') == "address":
>>>>>>> 35050159178fff696eb967b9356de09cc4dfb777
            new_address_record = AddressRequest(address = self.request.get('address'))
            new_address_record.put()
        else:
            logging.error("Malformed Request!")

<<<<<<< HEAD
class MapsHandler(webapp2.RequestHandler):
    def get(self):
        # All we need to do is really just displaying the page once.
        # From now on everything will be client-side, at least for now.
        template = JINJA_ENV.get_template('templates/maps.html')
        self.response.write(template.render())
=======
class MainHandler(webapp2.RequestHandler):
    def get(self):
        # All we need to do is really just displaying the page once.
        # From now on everything will be client-side, at least for now.
        template = JINJA_ENV.get_template('templates/map.html')
        self.response.write(template.render())

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/record_request', RecordRequestHandler)
], debug=True)
>>>>>>> 35050159178fff696eb967b9356de09cc4dfb777
