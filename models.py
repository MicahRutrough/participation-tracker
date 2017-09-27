################################################################################
## IMPORTS #####################################################################
################################################################################


from google.appengine.ext import ndb


################################################################################
################################################################################
################################################################################

class StudentGrades(ndb.Model):
        ucinetid   = ndb.StringProperty()
	grades     = ndb.StringProperty(repeated=True)
	quarter    = ndb.IntegerProperty() #0=fall, 1=winter, 2=spring, 3=summer
	year       = ndb.IntegerProperty()
	course     = ndb.StringProperty()

class Settings(ndb.Model):
	quarter    = ndb.IntegerProperty() #0=fall, 1=winter, 2=spring, 3=summer
	year       = ndb.IntegerProperty()
	course     = ndb.StringProperty()
