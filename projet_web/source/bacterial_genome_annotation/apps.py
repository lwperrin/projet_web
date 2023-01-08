
from django.apps import AppConfig

class MyAppConfig(AppConfig):
    name = 'bacterial_genome_annotation'
    verbose_name = "My app"

    def ready(self):
        import bacterial_genome_annotation.signals.handlers