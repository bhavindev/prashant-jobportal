from django.contrib import admin
from apps.servicepage.models import *

@admin.register(ServicePageSEO)
class ServicePageSEOAdmin(admin.ModelAdmin):
    list_display = ['meta_title', 'meta_description']