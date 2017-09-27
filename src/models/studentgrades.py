from models import StudentGrades
from google.appengine.ext import ndb
class StudentGradesModel:

    @staticmethod
    def get_grades_by_id(ucinetid, quarter, year, course):
        return StudentGrades.query(StudentGrades.ucinetid == ucinetid,
                                   StudentGrades.quarter  == quarter,
                                   StudentGrades.year     == year,
                                   StudentGrades.course   == course).get()

    @staticmethod
    def get_grade_headers(quarter, year, course):
        return StudentGrades.query(StudentGrades.ucinetid == "ucinetid",
                                   StudentGrades.quarter  == quarter,
                                   StudentGrades.year     == year,
                                   StudentGrades.course   == course).get()

    @staticmethod
    def get_total_grades(quarter, year, course):
        return StudentGrades.query(StudentGrades.ucinetid == "TOTAL",
                                   StudentGrades.quarter  == quarter,
                                   StudentGrades.year     == year,
                                   StudentGrades.course   == course).get()

    @staticmethod
    def get_all_grades(quarter, year, course):
        return StudentGrades.query(StudentGrades.ucinetid != "TOTAL",
                                   StudentGrades.ucinetid != "ucinetid",
                                   StudentGrades.quarter  == quarter,
                                   StudentGrades.year     == year,
                                   StudentGrades.course   == course)

    @staticmethod
    def get_all_keys():
        return StudentGrades.query()
