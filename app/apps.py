from django.apps import AppConfig

class AppConfig(AppConfig):
    name = 'app'

    def ready(self):
        import app.signals  # Ensure this is loading the signals file
