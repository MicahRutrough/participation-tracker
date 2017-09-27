from models import Settings
from google.appengine.ext import ndb
class SettingsModel:

    @staticmethod
    def get_current_settings():
        return Settings.query().get()
