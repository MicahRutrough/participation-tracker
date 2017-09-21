from models import StudentGrades
from google.appengine.ext import ndb
class StudentGradesModel:

    @staticmethod
    def get_grades_by_id(ucinetid):
        return StudentGrades.query(StudentGrades.ucinetid == ucinetid).get()

    @staticmethod
    def get_grade_headers():
        return StudentGrades.query(StudentGrades.ucinetid == "ucinetid").get()

    @staticmethod
    def get_total_grades():
        return StudentGrades.query(StudentGrades.ucinetid == "TOTAL").get()

    @staticmethod
    def get_all_grades():
        return StudentGrades.query(StudentGrades.ucinetid != "TOTAL",
                                   StudentGrades.ucinetid != "ucinetid")
