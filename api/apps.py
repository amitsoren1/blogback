from django.apps import AppConfig


class ApiConfig(AppConfig):
    name = 'api'

    def ready(self): #method just to import the signals
    	import api.signals