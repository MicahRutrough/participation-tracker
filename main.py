import webapp2
import sys
from src.controllers import landing
from src.controllers import admin
config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': 'some-secret-key',
}

application = webapp2.WSGIApplication([
    ('/', landing.Main),
    ('/grades', landing.MainPage),
    ('/admin', admin.ViewGrades),
    ('/admin/upload', admin.UploadGrades),
], config=config, debug=True)
