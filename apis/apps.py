from django.apps import AppConfig
import os

class ApisConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apis'

    started = False
    def ready(self):
        if not self.started and  os.environ.get('RUN_MAIN') == 'true':
            from certificate_app import schedular
            schedular.start()
            self.started = True
