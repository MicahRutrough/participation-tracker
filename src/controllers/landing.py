import jinja2
import os
import webapp2

from google.appengine.api import users
from google.appengine.ext import ndb
from webapp2_extras.appengine.users import login_required

from models import StudentGrades
from src.handler.base_handler import BaseHandler
from src.models.studentgrades import StudentGradesModel

JINJA_ENV = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname('app.yaml')),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class GradePage(BaseHandler):
    @login_required
    def get(self):
        
        user = users.get_current_user()
        headers = StudentGradesModel.get_grade_headers()
        totals =  StudentGradesModel.get_total_grades()
        grades =  StudentGradesModel.get_grades_by_id(str(user).split("@")[0])
        try:
            grade_info = zip(headers.grades,totals.grades,grades.grades)
        except AttributeError:
            grade_info = None
        
        template = JINJA_ENV.get_template("/templates/grades.html")
        template_values = {
            "user": user,
            "grade_info": grade_info,
            "sign_out":users.create_logout_url('/'),
        }
        return self.response.write(template.render(template_values))

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

        return self.response.write(template.render(template_values))

