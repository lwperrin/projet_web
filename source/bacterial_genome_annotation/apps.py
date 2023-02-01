from django.apps import AppConfig

class YourAppConfig(AppConfig):
    name = 'bacterial_genome_annotation'

    def ready(self):
        import bacterial_genome_annotation.signals.handlers
       
class ContactConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'contact'
