import jinja2
import os
import webapp2

from google.appengine.api import users
from google.appengine.ext import ndb
from webapp2_extras.appengine.users import login_required

from src.handler.base_handler import BaseHandler

JINJA_ENV = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname('app.yaml')),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainPage(BaseHandler):
    @login_required
    def get(self):
        template = JINJA_ENV.get_template("/templates/grades.html")
        user = users.get_current_user()
        grades = ["A","B","C"]#Get pull grades from the cloud
        template_values = {
            "user": user,
            "grades": grades,
            "sign_out":users.create_logout_url('/'),
        }
        self.response.write(template.render(template_values))

class Main(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        template = JINJA_ENV.get_template('/templates/index.html')
        template_values = {}

        if user:
            template_values['user'] = user.email()
            template_values['sign_out'] = users.create_logout_url('/')
        else:
            template_values['sign_in'] = users.create_login_url('/grades')

        self.response.write(template.render(template_values))

