import webapp2
import os
import jinja2

from google.appengine.api import users
from google.appengine.ext import ndb

jinja_env = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
)

class User(ndb.Model):
    first_name = ndb.StringProperty()
    last_name = ndb.StringProperty()

class LoginHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            form_template = jinja_env.get_template('templates/login.html')
            html = form_template.render()
            self.response.write(html)
            email_address = user.nickname()
            user = User.get_by_id(user.user_id())
            signout_link_html = '<a href="%s">sign out</a>' % (users.create_logout_url('/'))
            if user:
                self.response.write('''Welcome %s %s (%s)! <br>''' %(user.frist_name,
                user.last_name,
                email_address,
                signout_link_html))
            else:
                form_template = jinja_env.get_template('templates/login.html')
                html = form_template.render()
                self.response.write(html)
                self.response.write('''
                Welcome to our site, %s! Please sign up! <br>
                <form method="post" action="/">
                <input type="text" name="first_name">
                <input type="text" name="last_name"
                <input type="submit">
                </form><br> %s <br>''' % (email_address, signout_link_html))
        else:
            template_data = {'login_link': users.create_login_url('/')}
            login_template = jinja_env.get_template('templates/login_link.html')
            html2 = login_template.render(template_data)
            self.response.write(html2)
            return

    def post(self):
        user = users.get_current_user()
        if not user:
            self.error(500)
            return
        user = user(frist_name = self.request.get('first_name'),
            last_name=self.request.get('last_name'),
            id=user.user_id())
        user.put()
        self.response.write("Thanks for signing up, %s!" % user.first_name)
