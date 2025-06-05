from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Create a superuser with a specified password, run migrations, and collect static files'

    def handle(self, *args, **options):
        # Run migrations
        self.stdout.write('Running migrations...')
        call_command("makemigrations", interactive=False)
        call_command("migrate", interactive=False)
        self.stdout.write(self.style.SUCCESS('Migrations completed.'))

        # Collect static files
        self.stdout.write('Collecting static files...')
        call_command("collectstatic", interactive=False)
        self.stdout.write(self.style.SUCCESS('Static files collected successfully.'))
        
        # Define superuser information
        username = 'admin'
        email = 'admin@gmail.com'
        password = '123456'

        # Create a superuser if it doesn't already exist
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_superuser(username, email, password)
            self.stdout.write(self.style.SUCCESS(f'Superuser "{username}" created successfully.'))
        else:
            self.stdout.write(self.style.ERROR(f'Superuser with username "{username}" already exists.'))