from django.apps import AppConfig


class UweflixConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'UWEFlix'

    def ready(self):
        from .models import update_films  # import your function here
        update_films()
