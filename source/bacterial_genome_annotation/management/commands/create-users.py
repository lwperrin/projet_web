from django.core.management.base import BaseCommand
from ...models import User
from django.contrib.auth.models import Group
import os.path
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
        
        with open(os.path.dirname(__file__) + '/../../assets/default_users.txt') as file:
            lines = file.readlines()
            while lines[0].startswith('#'):
                lines = lines[1:]
            lines = lines[1:]
            while len(lines)!=0:
                email = lines[0][:-1]
                password = lines[1][:-1]
                group = lines[2][:-1]
                User.objects.create_user(email, password)
                print(email)
                print('a')
                u = User.objects.get(email=email)
                if group=='Annotators':
                    u.groups.add(annotators)
                elif group=='Validators':
                    u.groups.add(annotators)
                    u.groups.add(validators)
                elif group=='Admins':
                    u.groups.add(annotators)
                    u.groups.add(validators)
                    u.groups.add(admins)
                lines = lines[4:]
        