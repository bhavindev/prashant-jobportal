from django.core.management.base import BaseCommand
from django.db import models
from django.apps import apps
import os

class Command(BaseCommand):
    help = 'Automatically update all CharField max_length values to 255 if they exceed 255.'

    def handle(self, *args, **kwargs):
        for model in apps.get_models():
            model_file = self.get_model_file(model)
            if model_file:
                changed = False
                model_name = model.__name__
                self.stdout.write(self.style.NOTICE(f"Checking model {model_name}..."))
                
                # Iterate over each field in the model
                for field in model._meta.fields:
                    if isinstance(field, models.CharField) and field.max_length > 255:
                        # Log the change
                        self.stdout.write(self.style.SUCCESS(f"Updating {field.name} in {model_name} (max_length={field.max_length})"))
                        # Update the field definition in the file
                        self.update_field_max_length(model_file, field.name, field.max_length)

                        changed = True

                if changed:
                    self.stdout.write(self.style.WARNING(f"Updated file {model_file} for {model_name}"))
            else:
                self.stdout.write(self.style.ERROR(f"Couldn't find model file for {model.__name__}"))

    def get_model_file(self, model):
        """Find the model's file path by checking the model's module"""
        try:
            module = model.__module__
            module_file = module.replace('.', '/') + '.py'
            if os.path.exists(module_file):
                return module_file
            return None
        except Exception as e:
            return None

    def update_field_max_length(self, model_file, field_name, current_max_length):
        """Update the max_length value in the model's file"""
        try:
            with open(model_file, 'r') as file:
                lines = file.readlines()

            with open(model_file, 'w') as file:
                for line in lines:
                    if f"{field_name} = models.CharField" in line and f"max_length={current_max_length}" in line:
                        # Replace the old max_length with 255
                        line = line.replace(f"max_length={current_max_length}", "max_length=255")
                    file.write(line)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error updating field {field_name} in {model_file}: {str(e)}"))