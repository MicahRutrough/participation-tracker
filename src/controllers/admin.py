import jinja2
import os

from google.appengine.api import users
from google.appengine.ext import ndb
from webapp2_extras.appengine.users import admin_required

from models import StudentGrades
from src.handler.base_handler import BaseHandler
from src.models.studentgrades import StudentGradesModel

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
            file = self.request.get('the_file')
            file = file.strip().split('\n')
            student_grades = []
            existing_grades = map(lambda x: x.ucinetid, StudentGradesModel.get_all_grades())
            for row in file:
                row = row.replace('"','').strip().split(',')
                dataid = row[0]
                if dataid == "ucinetid" or dataid == "TOTAL":
                    info = StudentGradesModel.get_grades_by_id(dataid)
                    if info == None:
                        info = StudentGrades()
                        info.ucinetid=dataid
                    info.grades = row[1:]
                    info.put()
                else:
                    if dataid not in existing_grades:
                        new_grades = StudentGrades()
                        new_grades.ucinetid = dataid
                        new_grades.grades = row[1:]
                        student_grades.append(new_grades)
                    else:
                        current_grade = StudentGradesModel.get_grades_by_id(dataid)
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
        
        headers = StudentGradesModel.get_grade_headers()
        if headers != None:
            headers = headers.grades
        else:
            headers = []

            
        totals = StudentGradesModel.get_total_grades()
        if totals != None:
            totals = totals.grades
        else:
            totals = []
        
        grades = StudentGradesModel.get_all_grades()
        if grades == None:
            grades = []
        else:
            grades = sorted(grades, key=(lambda x: x.ucinetid))

            
        template        = JINJA_ENV.get_template('/templates/admin_view.html')
        template_values = {                            
            'user':         users.get_current_user(),
            'sign_out':     users.create_logout_url('/'),
            'message':      self.request.get('message'),
            'headers':       headers,
            'totals':       totals,
            'grades':       grades,
        }
        return self.response.write(template.render(template_values))        


