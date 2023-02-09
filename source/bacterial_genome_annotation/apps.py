"""
This file defines the AppConfig. It is usefully to link the signals to the application.
"""

from django.apps import AppConfig

class MyAppConfig(AppConfig):
    name = 'bacterial_genome_annotation'
    default_auto_field = 'django.db.models.BigAutoField'

    def ready(self):
        import bacterial_genome_annotation.signals.handlers
       
"""class ContactConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'contact'"""
