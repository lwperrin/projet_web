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
            name='Can annotate',
            content_type=content_type,
        )

        canValidate, created = Permission.objects.get_or_create(
            codename='can_validate',
            name='Can validate',
            content_type=content_type,
        )

        canAssign, created = Permission.objects.get_or_create(
            codename='can_assign',
            name='Can assign',
            content_type=content_type,
        )

        canPromoteAnnotator, created = Permission.objects.get_or_create(
            codename='can_promote_annotator',
            name='Can promote to annotator',
            content_type=content_type,
        )

        canPromoteValidator, created = Permission.objects.get_or_create(
            codename='can_promote_validator',
            name='Can promote to validator',
            content_type=content_type,
        )

        canPromoteAdmin, created = Permission.objects.get_or_create(
            codename='can_promote_admin',
            name='Can promote to admin',
            content_type=content_type,
        )

        canDowngrade, created = Permission.objects.get_or_create(
            codename='can_downgrade',
            name='Can downgrade',
            content_type=content_type,
        )

        grps = [Group.objects.get_or_create(name=n)[0] for n in ['reader', 'annotator', 'validator', 'admin']]
        for i in range(0, 4):  # Readers
            pass
        for i in range(1, 4):  # Annotators
            grps[i].permissions.add(canAnnotate)
        for i in range(2, 4):  # Validators
            grps[i].permissions.add(canValidate)
            grps[i].permissions.add(canAssign)
            grps[i].permissions.add(canPromoteAnnotator)
        for i in range(3, 4):  # Admins
            grps[i].permissions.add(canPromoteValidator)
            grps[i].permissions.add(canPromoteAdmin)
            grps[i].permissions.add(canDowngrade)
        for g in grps:
            g.save()
