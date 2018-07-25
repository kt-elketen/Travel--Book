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

#class CoordsRequest(ndb.Model):
#    lat = ndb.StringProperty(required = True)
#    lon = ndb.StringProperty(required = True)
#    timestamp = ndb.DateTimeProperty(auto_now_add = True)

class AddressRequest(ndb.Model):
    address = ndb.StringProperty(required = True)
    timestamp = ndb.DateTimeProperty(auto_now_add = True)

class RecordRequestHandler(webapp2.RequestHandler):
    def post(self):
        logging.info(self.request)
        if  self.request.get('type') == "address":
            new_address_record = AddressRequest(address = self.request.get('address'))
            new_address_record.put()
        else:
            logging.error("Malformed Request!")

class MapsHandler(webapp2.RequestHandler):
    def get(self):
        # All we need to do is really just displaying the page once.
        # From now on everything will be client-side, at least for now.
        template = JINJA_ENV.get_template('templates/maps.html')
        self.response.write(template.render())
