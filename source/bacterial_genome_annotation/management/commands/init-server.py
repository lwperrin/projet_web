from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):

    def handle(self, *args, **options):
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
