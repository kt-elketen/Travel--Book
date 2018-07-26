import webapp2
import os
import jinja2
import login
import maps
from google.appengine.api import images
#remember, you can get this by searching for jinja2 google app engine
#jinja_current_dir = jinja2.Environment(
#    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
#    extensions=['jinja2.ext.autoescape'],
#    autoescape=True)

jinja_env = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        form_template = jinja_env.get_template('templates/homepage.html')
        html = form_template.render()
        self.response.write(html)

class TripsHandler(webapp2.RequestHandler):
    def get(self):
        pass
class TripListHandler(webapp2.RequestHandler):
    def get(self):
        form_template = jinja_env.get_template('templates/triplist.html')
        html = form_template.render()
        self.response.write(html)
        pass
class TripTimelineHandler(webapp2.RequestHandler):
    def get(self):
        timeline_data = {
        'picture_date': Pictures.date,
        'picture_place': Pictures.location,
        'picture_description': Pictures.description,
        'trip_name': Trip.name
        }
        form_template = jinja_env.get_template('templates/triptimeline.html')
        html = form_template.render(timeline_data)
        self.response.write(html)


class UploadHandler(webapp2.RequestHandler):
    def get(self):
        form_template = jinja_env.get_template('templates/upload.html')
        html = form_template.render()
        self.response.write(html)
    def post(self):
        Trip.name = self.request.get('trip')
        Pictures.location = self.request.get('location')
        Pictures.date = self.request.get('date')
        Pictures.description = self.request.get('description')
        Pictures.comments = self.request.get('comments')
        Pictures.information = self.request.get('information')
        Pictures.image = images.resize(self.request.get('image'), 250, 250)
        Pictures.put()

# Model for an image:
from google.appengine.ext import ndb
class Pictures(ndb.Model):
    location = ndb.StringProperty(required = True)
    date = ndb.StringProperty(required = True)
    description = ndb.StringProperty(required = False)
    comments = ndb.StringProperty(required = False)
    image = ndb.BlobProperty(required = True)
class Trip(ndb.Model):
    name = ndb.StringProperty(required= True)
    pictures = ndb.KeyProperty(Pictures, repeated= True)



class Image(webapp2.RequestHandler):
    def get(self):
        key = ndb.Key("Pictures", int(self.request.get("id")))
        data = key.get()
        self.response.headers['Content-Type'] = 'image/jpg'
        self.response.write(data.image)




app = webapp2.WSGIApplication([
      ('/', MainHandler),
      ('/login', login.LoginHandler),
      ('/trips', TripsHandler),
      ('/triplist', TripListHandler),
      ('/maps', maps.MapsHandler),
      ('/maps/record_request', maps.RecordRequestHandler),
      ('/upload', UploadHandler),
      ('/img', Image),
      ('/triptimeline', TripTimelineHandler)
], debug=True)
