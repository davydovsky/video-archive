from django.core.management import BaseCommand, call_command, CommandError


class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            call_command('createsuperuser', '--noinput', interactive=False)
        except CommandError:
            # In case the superuser already exists just pass
            pass
