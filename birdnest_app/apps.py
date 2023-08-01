from django.apps import AppConfig
from django.conf import settings

class BirdnestAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'birdnest_app'

    def ready(self) -> None:
        super().ready()
        if settings.SCHEDULER_DEFAULT:
            from birdnest_backend import operators
            operators.start()