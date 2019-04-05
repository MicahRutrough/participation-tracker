import jinja2
import os

from google.appengine.api import users
from google.appengine.ext import ndb
from webapp2_extras.appengine.users import admin_required

from models import StudentGrades, Settings
from src.handler.base_handler import BaseHandler
from src.models.studentgrades import StudentGradesModel
from src.models.settings import SettingsModel

JINJA_ENV = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname('app.yaml')),
    extensions = ['jinja2.ext.autoescape'],
    autoescape=True)

class UploadGrades(BaseHandler):
    
    @admin_required
    def get(self):
        template_values = {                                                        
            'user':     users.get_current_user(),
            'sign_out': users.create_logout_url('/'),
            'message':  self.request.get('message'),
        }
        template = JINJA_ENV.get_template('/templates/admin_upload.html')
        return self.response.write(template.render(template_values))            


    def post(self):
        try:
            settings = SettingsModel.get_current_settings()
            if settings == None:
                assert False, "Settings for this quarter have not been set up"
            else:
                QUARTER = settings.quarter
                YEAR = settings.year
                COURSE = settings.course

            file = self.request.get('the_file')
            file = file.strip().split('\n')
            student_grades = []
            existing_grades = map(lambda x: x.ucinetid, StudentGradesModel.get_all_grades(QUARTER,YEAR,COURSE))
            for row in file:
                row = row.replace('"','').strip().split(',')
                dataid = row[0]
                if dataid == "ucinetid" or dataid == "TOTAL":
                    info = StudentGradesModel.get_grades_by_id(dataid,QUARTER,YEAR,COURSE)
                    if info == None:
                        info = StudentGrades()
                        info.ucinetid=dataid
                        info.quarter=QUARTER
                        info.year=YEAR
                        info.course=COURSE
                    info.grades = row[1:]
                    info.put()
                else:
                    if dataid not in existing_grades :
                        new_grades = StudentGrades()
                        new_grades.ucinetid = dataid
                        new_grades.quarter=QUARTER
                        new_grades.year=YEAR
                        new_grades.course=COURSE
                        new_grades.grades = row[1:]
                        student_grades.append(new_grades)
                    else:
                        current_grade = StudentGradesModel.get_grades_by_id(dataid,QUARTER,YEAR,COURSE)
                        if "".join(current_grade.grades).rstrip('0') != "".join(row[1:]).rstrip('0') or len(current_grade.grades) > len(row[1:]):
                            current_grade.grades = row[1:]
                            current_grade.put()
                        
            # save student objects...
            ndb.put_multi(student_grades)
            # ...and render the response
            return self.redirect('/admin?message=' + 'Successfully uploaded new participation')            

        except Exception, e:
            return self.redirect('/admin/upload?message=' + 'There was a problem uploading the participation: ' + str(e))            


class ViewGrades(BaseHandler):
    @admin_required
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
            
        headers = StudentGradesModel.get_grade_headers(QUARTER,YEAR,COURSE)
        if headers != None:
            headers = headers.grades
        else:
            headers = []
            
        totals = StudentGradesModel.get_total_grades(QUARTER,YEAR,COURSE)
        if totals != None:
            totals = totals.grades
        else:
            totals = []
        
        grades = StudentGradesModel.get_all_grades(QUARTER,YEAR,COURSE)
        if grades == None:
            grades = []
        else:
            grades = sorted(grades, key=(lambda x: x.ucinetid))
            for i in range(len(grades)):
                if len(grades[i].grades) < len(totals):
                    for j in range(len(headers) - len(grades[i].grades)):
                        grades[i].grades.append(0)

            
        template        = JINJA_ENV.get_template('/templates/admin_view.html')
        template_values = {                            
            'user':         users.get_current_user(),
            'sign_out':     users.create_logout_url('/'),
            'message':      self.request.get('message'),
            'headers':      headers,
            'totals':       totals,
            'grades':       grades,
            'settings':     settings,
            'ref': ['Fall','Winter','Spring','Summer'],
        }
        return self.response.write(template.render(template_values))        

class ChangeSettings(BaseHandler):
    @admin_required
    def get(self):
        settings = SettingsModel.get_current_settings()
        template_values = {                                                        
            'user':     users.get_current_user(),
            'settings': settings,
            'ref': ['Fall','Winter','Spring','Summer'],
            'sign_out': users.create_logout_url('/'),
            'message':  self.request.get('message'),
        }
        template = JINJA_ENV.get_template('/templates/admin_settings.html')
        return self.response.write(template.render(template_values))

    def post(self):
        try:
            delete = str(self.request.get('delete'))
            if delete == "I wish to delete all records":
                all_keys = StudentGradesModel.get_all_keys()
                for a in all_keys:
                    a.key.delete()
                return self.redirect('/admin?message=' + 'RECORDS DELETED')
            quarter = int(self.request.get('quarter'))
            year = int(self.request.get('year'))
            course = str(self.request.get('course'))

            current_settings = SettingsModel.get_current_settings()
            if current_settings == None:
                new_settings = Settings()
                new_settings.quarter = quarter
                new_settings.year = year
                new_settings.course = course
                new_settings.put()
            else:
                current_settings.quarter = quarter
                current_settings.year = year
                current_settings.course = course
                current_settings.put()
            
            return self.redirect('/admin?message=' + 'Successfully changed settings')
        except Exception, e:
            return self.redirect('/admin/settings?message=' + 'There was a problem changing the settings: ' + str(e))     
