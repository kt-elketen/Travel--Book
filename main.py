import webapp2
import os
import jinja2
import login
from google.appengine.api import images
from google.appengine.ext import ndb
from google.appengine.ext import blobstore

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
        template_data = {}
        trips = Trip.query().fetch()
        form_template = jinja_env.get_template('templates/triplist.html')
        for trip in trips:
            template_data[trip.pictures[0].urlsafe()] = trip
        html = form_template.render({
            'trips': template_data,
        })

        # blob_key = self.request.get("blob_key")
        # if blob_key:
        #     blob_info = blobstore.get(blob_key)
        #
        #     if blob_info:
        #         img = images.Image(blob_key=blob_key)
        #         img.im_feeling_lucky()
        #         thumbnail = img.execute_transforms(output_encoding=images.JPEG)
        #
        #         self.response.headers['Content-Type'] = 'image/jpeg'
        #         self.response.out.write(thumbnail)
        #         return
        # url = images.get_serving_url(
        #     blob_key, secure_url=True)
        self.response.write(html)

        #all_trips = Trip.query().fetch()

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

class NewTripHandler(webapp2.RequestHandler):
    def get(self):
        form_template = jinja_env.get_template('templates/new_trip.html')
        html = form_template.render()
        self.response.write(html)
    def post(self):
        picture = Picture()
        picture.image = images.resize(self.request.get('image'), 250, 250)
        # picture_key = picture.put()
        picture.put()
        trip = Trip()
        trip.name=self.request.get('trip')
        # trip.pictures=[picture_key]
        trip.put()
        self.redirect("/newpicture")

# Model for an image:
class Picture(ndb.Model):
    location = ndb.StringProperty(required = True)
    date = ndb.StringProperty(required = True)
    description = ndb.StringProperty(required = False)
    image = ndb.BlobProperty(required = True)

class Trip(ndb.Model):
    name = ndb.StringProperty(required = True)
    pictures = ndb.KeyProperty(Picture, repeated = True)
    thumbnail = ndb.StringProperty(required = False)

class NewPictureHandler(webapp2.RequestHandler):
    def get(self):
        template_data = {}
        trips = Trip.query().fetch()
        form_template = jinja_env.get_template('templates/New_picture.html')
        for trip in trips:
            template_data[trip.name] = trip
        html = form_template.render({
            'trips': template_data
        })
        print(trips)
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
      ('/newpicture', NewPictureHandler),
      ('/img', Image),
      ('/triptimeline', TripTimelineHandler),
      ('/newtrip', NewTripHandler)
], debug=True)
