from django.apps import AppConfig


class MoriaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'moria'

    def ready(self):
        import moria.signals
