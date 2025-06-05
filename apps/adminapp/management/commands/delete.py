import os
from django.core.management.base import BaseCommand
from django.apps import apps

class Command(BaseCommand):
    help = 'Delete all migration files except __init__.py from the apps migrations folder'

    def handle(self, *args, **options):
        for app_config in apps.get_app_configs():
            migrations_dir = os.path.join(app_config.path, 'migrations')
            if os.path.exists(migrations_dir):
                self.stdout.write(f'Deleting migration files in {app_config.label}...')
                for filename in os.listdir(migrations_dir):
                    if filename.endswith('.py') and filename != '__init__.py':
                        migration_file = os.path.join(migrations_dir, filename)
                        os.remove(migration_file)
                        self.stdout.write(f'Deleted {filename}')
                self.stdout.write(f'Deleted all migration files in {app_config.label}')
            else:
                self.stdout.write(f'No migrations folder found in {app_config.label}')

        self.stdout.write(self.style.SUCCESS('Successfully deleted migration files'))