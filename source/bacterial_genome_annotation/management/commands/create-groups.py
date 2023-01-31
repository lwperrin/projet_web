from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from bacterial_genome_annotation.models import User
from os.path import dirname

class Command(BaseCommand):
    def add_arguments(self, parser):
        # Positional arguments
        pass

    def handle(self, *args, **kwargs):
        content_type = ContentType.objects.get_for_model(User)
        
        canAnnotate, created = Permission.objects.get_or_create(
            codename='can_annotate',
            name='Can Annotate',
            content_type=content_type,
        )
        
        grps = [Group.objects.get_or_create(name=n)[0] for n in ['reader', 'annotator', 'validator', 'admin']]
        grps[1].permissions.add(canAnnotate)
        grps[2].permissions.add(canAnnotate)
        grps[3].permissions.add(canAnnotate)
        for g in grps:
            g.save()