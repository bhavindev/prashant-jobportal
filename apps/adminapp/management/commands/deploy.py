from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError

class Command(BaseCommand):
    help = 'Install TCG CRM with a superuser'

    def handle(self, *args, **options):
        username = 'admin'
        email = 'admin@gmail.com'
        password = '123456'

        # Running migrations
        self.stdout.write(self.style.NOTICE('Running migrations...'))
        call_command('migrate')

        # Running collectstatic
        self.stdout.write(self.style.NOTICE('Collecting static files...'))
        call_command('collectstatic', interactive=False)  # 'interactive=False' to avoid user prompts

        User = get_user_model()

        try:
            if User.objects.filter(username=username).exists():
                self.stdout.write(self.style.WARNING(f"User with username '{username}' already exists."))
            else:
                User.objects.create_superuser(username=username, email=email, password=password)
                self.stdout.write(self.style.SUCCESS(f"Superuser '{username}' created successfully."))
        except IntegrityError:
            self.stdout.write(self.style.ERROR('Failed to create the superuser due to an integrity error.'))