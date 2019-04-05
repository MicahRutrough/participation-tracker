import jinja2
import os
import webapp2
import datetime

from google.appengine.api import users
from google.appengine.ext import ndb
from webapp2_extras.appengine.users import login_required

from models import StudentGrades, Settings
from src.handler.base_handler import BaseHandler
from src.models.studentgrades import StudentGradesModel
from src.models.settings import SettingsModel

JINJA_ENV = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname('app.yaml')),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

TIME_DELTA = -7

class GradePage(BaseHandler):
    @login_required
    def get(self):

        settings = SettingsModel.get_current_settings()
        if settings == None:
            QUARTER = 0
            YEAR = 0
            COURSE = ""
        else:
            QUARTER = settings.quarter
            YEAR = settings.year
            COURSE = settings.course

        current_datetime = datetime.datetime(2000,01,01).now()+datetime.timedelta(hours=TIME_DELTA)
        user = users.get_current_user()
        headers = StudentGradesModel.get_grade_headers(QUARTER,YEAR,COURSE)
        totals =  StudentGradesModel.get_total_grades(QUARTER,YEAR,COURSE)
        grades =  StudentGradesModel.get_grades_by_id(str(user).split("@")[0],QUARTER,YEAR,COURSE)
        try:
            dates = map(lambda x: datetime.datetime(2000,01,01).strptime(x, "%Y-%m-%d %H:%M:%S")+datetime.timedelta(hours=TIME_DELTA),headers.grades)
            if len(grades.grades) < len(headers.grades):
                for i in range(len(headers.grades) - len(grades.grades)):
                    grades.grades.append(0)
            grade_info = zip(map(lambda x: ((datetime.datetime(2000,01,01).strptime(x, "%Y-%m-%d %H:%M:%S")+datetime.timedelta(hours=TIME_DELTA)).strftime("%A, %B %d, %Y at %I:%M %p")),headers.grades),totals.grades,grades.grades,dates)
        except AttributeError:
            grade_info = None
    
        template = JINJA_ENV.get_template("/templates/grades.html")
        template_values = {
            "user": user,
            "current_datetime": current_datetime,
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

class Help(webapp2.RequestHandler):
    def get(self):

        user = users.get_current_user()
        template = JINJA_ENV.get_template('/templates/instructions.html')
        template_values = {}

        if user:
            template_values['user'] = user.email()
            template_values['sign_out'] = users.create_logout_url('/')
        else:
            template_values['sign_in'] = users.create_login_url('/grades')

        return self.response.write(template.render(template_values))


