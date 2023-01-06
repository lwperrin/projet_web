from django.core.management.base import BaseCommand
from ...models import User
from django.contrib.auth.models import Group

class Command(BaseCommand):
    def add_arguments(self, parser):
        # Positional arguments
        pass

    def handle(self, *args, **kwargs):
        readers, isCreate = Group.objects.get_or_create(name='Readers')
        annotators, isCreate = Group.objects.get_or_create(name='Annotators')
        validators, isCreate = Group.objects.get_or_create(name='Validators')
        admins, isCreate = Group.objects.get_or_create(name='Admins')
        User.objects.create_user(email='admin@admin.com',
                                password='Ac1net0bactErb@umannii',
                                is_staff=True,
                                is_active=True,
                                is_superuser=True)
        admin = User.objects.get(email='admin@admin.com')
        admin.groups.add(annotators)
        admin.groups.add(validators)
        admin.groups.add(admins)
        