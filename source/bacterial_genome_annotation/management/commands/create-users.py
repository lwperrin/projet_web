"""
This is the command to create a bunch of users based on the file default_users.txt.
"""

from django.core.management.base import BaseCommand
from ...models import User
from django.contrib.auth.models import Group
from os.path import dirname


class Command(BaseCommand):
    def add_arguments(self, parser):
        # Positional arguments
        pass

    def handle(self, *args, **kwargs):
        """
        The handle function creates a default admin user and adds the default users to the database.
        It also assigns each user to their respective group.

        :param self: Access the attributes and methods of the class in python
        :param *args: Pass a non-keyworded, variable-length argument list to the function
        :param **kwargs: Pass in any additional keyword arguments (**kwargs) to the function
        """
        grps = [Group.objects.get_or_create(name=n)[0] for n in ['reader', 'annotator', 'validator', 'admin']]
        try:
            User.objects.create_user(email='admin@admin.com',
                                     password='Ac1net0bactErb@umannii',
                                     is_staff=True,
                                     is_active=True,
                                     is_superuser=True)
        except:
            pass
        admin = User.objects.get(email='admin@admin.com')
        admin.groups.add(grps[0])
        admin.groups.add(grps[1])
        admin.groups.add(grps[2])
        admin.groups.add(grps[3])

        with open(dirname(__file__) + '/../../assets/default_users.txt') as file:
            lines = file.readlines()
            while lines[0].startswith('#'):
                lines = lines[1:]
            lines = lines[1:]
            while len(lines) != 0:
                email = lines[0][:-1]
                password = lines[1][:-1]
                group = lines[2][:-1]
                try:
                    User.objects.create_user(email, password)
                except:
                    pass
                u = User.objects.get(email=email)
                if group == grps[0].name:
                    u.groups.add(grps[0])
                elif group == grps[1].name:
                    u.groups.add(grps[0])
                    u.groups.add(grps[1])
                elif group == grps[2].name:
                    u.groups.add(grps[0])
                    u.groups.add(grps[1])
                    u.groups.add(grps[2])
                elif group == grps[3].name:
                    u.groups.add(grps[0])
                    u.groups.add(grps[1])
                    u.groups.add(grps[2])
                    u.groups.add(grps[3])
                lines = lines[4:]
                u.save()
        for g in grps:
            g.save()
