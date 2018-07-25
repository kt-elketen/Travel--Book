import webapp2
import os
import jinja2
import login


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


class UploadHandler(webapp2.RequestHandler):
    def get(self):
        # form_template = jinja_env.get_template('templates/upload.html')
        # html = form_template.render()
        # self.response.write(html)

class ImageHandler(webapp2.RequestHandler):
    def get(self):
        key = ndb.Key("Data", int(self.request.get("id")))
        data = key.get()
        self.response.headers['Content-Type'] = 'image/jpg'
        self.response.write(data.image)




app = webapp2.WSGIApplication([
      ('/', MainHandler),
      ('/login', login.LoginHandler),
      ('/trips', TripsHandler),
      ('/upload', UploadHandler),
      ('/img', ImageHandler),
      ('/triplist', TripListHandler) 
], debug=True)
