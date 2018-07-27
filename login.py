import webapp2
import os
import jinja2

from google.appengine.api import users
from google.appengine.ext import ndb

jinja_env = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
)

class TravelUser(ndb.Model):
    first_name = ndb.StringProperty()
    last_name = ndb.StringProperty()

class LoginHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            email_address = user.nickname()
            traveluser = TravelUser.get_by_id(user.user_id())
            signout_link_html = ('<a href="%s">Sign Out</a>' % (users.create_logout_url('/logout')))
            if traveluser:
                self.response.write('''Welcome %s %s (%s)! <br> %s''' %(traveluser.first_name,
                traveluser.last_name,
                email_address,
                signout_link_html))
            else:
                signup_data = {
                'logout_link': signout_link_html
                }
                signup_template = jinja_env.get_template('templates/welcomepage.html')
                html3 = signup_template.render(signup_data)
                self.response.write(html3)

        else:
            login_data = {'login_link': users.create_login_url('/')}
            login_template = jinja_env.get_template('templates/login_link.html')
            html2 = login_template.render(login_data)
            self.response.write(html2)
            return

    def post(self):
        user = users.get_current_user()
        if not user:
            self.error(500)
            return
        user = TravelUser(first_name = self.request.get('first_name'),
            last_name=self.request.get('last_name'),
            id=user.user_id())
        user.put()
        self.response.write("Thanks for signing up, %s!" % user.first_name)
        self.redirect('/triplist')
