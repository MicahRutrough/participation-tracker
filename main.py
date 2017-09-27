import webapp2
import sys
from src.controllers import main
from src.controllers import admin
config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': 'some-secret-key',
}

application = webapp2.WSGIApplication([
    ('/', main.Main),
    ('/grades', main.GradePage),
    ('/admin', admin.ViewGrades),
    ('/admin/upload', admin.UploadGrades),
    ('/admin/settings', admin.ChangeSettings),
    ('/instructions', main.Help),
], config=config, debug=True)
