import webapp2
import os
import jinja2
import login
import maps


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
        form_template = jinja_env.get_template('templates/triptimeline.html')
        html = form_template.render()
        self.response.write(html)
        pass


class UploadHandler(webapp2.RequestHandler):
    def get(self):
        form_template = jinja_env.get_template('templates/upload.html')
        html = form_template.render()
        self.response.write(html)
    def post(self):
        data = Data()
        data.trip = self.request.get('trip')
        data.location = self.request.get('location')
        data.date = self.request.get('date')
        data.description = self.request.get('description')
        data.comments = self.request.get('comments')
        data.information = self.request.get('information')
        data.image = image.resize(self.request.get('image'), 250, 250)
        data.put()

# Model for an image:
from google.appengine.ext import ndb
class Data(ndb.Model):
    trip = ndb.StringProperty(required = True)
    location = ndb.StringProperty(required = True)
    date = ndb.StringProperty(required = True)
    description = ndb.StringProperty(required = False)
    comments = ndb.StringProperty(required = False)
    information = ndb.StringProperty(required = False)
    image = ndb.BlobProperty(required = True)




class Image(webapp2.RequestHandler):
    def get(self):
        key = ndb.Key("Data", int(self.request.get("id")))
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
