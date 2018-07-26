import webapp2
import os
import jinja2
import login
from google.appengine.api import images
from google.appengine.ext import ndb
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

class TripTimelineHandler(webapp2.RequestHandler):
    def get(self):
        form_template = jinja_env.get_template('templates/triptimeline.html')
        html = form_template.render()
        self.response.write(html)
        pass

# Model for an image:
class Picture(ndb.Model):
    location = ndb.StringProperty(required = True)
    date = ndb.StringProperty(required = True)
    description = ndb.StringProperty(required = False)
    image = ndb.BlobProperty(required = True)

class Trip(ndb.Model):
    name = ndb.StringProperty(required = True)
    pictures = ndb.KeyProperty(Picture, repeated = True)

class UploadHandler(webapp2.RequestHandler):
    def get(self):
        form_template = jinja_env.get_template('templates/upload.html')
        html = form_template.render()
        self.response.write(html)
    def post(self):
        picture = Picture()
        picture.location = self.request.get('location')
        picture.date = self.request.get('date')
        picture.description = self.request.get('description')
        picture.image = images.resize(self.request.get('image'), 250, 250)
        picture_key =picture.put()
        trip = Trip()
        trip.name=self.request.get('trip')
        trip.pictures=[picture_key]
        trip.put()
        self.redirect("/triplist")

class Image(webapp2.RequestHandler):
    def get(self):
        #key = ndb.Key("Data", int(self.request.get("id")))
        #data = key.get()
        #self.response.headers['Content-Type'] = 'image/jpg'
        #self.response.write(data.image)
        key = ndb.Key(urlsafe=self.request.get('img_id'))
        data = key.get()
        if data.image:
            self.response.headers['Content-Type'] = 'image/png'
            self.response.out.write(data.image)
        else:
            self.response.out.write('No image')
        self.response.out.write('<div><img src="/img?img_id=%s"></img>' %
                        data.key.urlsafe())
        #self.response.out.write('<blockquote>%s</blockquote></div>' %
        #                cgi.escape(data.content))




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
