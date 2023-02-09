"""
This is the all-in-one command to initialize the server. To prepare the database, just run :
.. code-block:: python

   python source/manage.py init-server

"""

from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):

    def handle(self, *args, **options):
        """
        The handle function is the entry point to this management command.
        This is an all-in-one command that calls each other command to initialize the server database.

        :param self: Access the attributes and methods of the class
        :param *args: Allow the function to take any number of arguments
        :param **options: Specify the optional arguments of the handle function
        """
        self.stdout.write(self.style.SUCCESS("***Making migrations***"))
        call_command('makemigrations')
        self.stdout.write(self.style.SUCCESS("***Performing migrations***"))
        call_command('migrate')
        self.stdout.write(self.style.SUCCESS("***Importing data***"))
        call_command('import-my-data')
        self.stdout.write(self.style.SUCCESS("***Creating groups and permissions***"))
        call_command('create-groups')
        self.stdout.write(self.style.SUCCESS(
            "***Creating users from default_users.txt***"))
        call_command('create-users')
        self.stdout.write(self.style.SUCCESS("=================="))
        self.stdout.write(self.style.SUCCESS(
            "The server is initialized and ready to be launched !"))
