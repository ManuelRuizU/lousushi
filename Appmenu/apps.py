# Appmenu/apps.py

from django.apps import AppConfig


class AppmenuConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Appmenu'

    def ready(self):
        import Appmenu.signals  # Importa el archivo signals.py
