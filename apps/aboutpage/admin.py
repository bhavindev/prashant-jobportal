from django.contrib import admin
from .models import *

@admin.register(aboutSettings)
class AboutSettingsAdmin(admin.ModelAdmin):
    list_display = ('title_white', 'title_red')
    
@admin.register(teamSection)
class TeamSectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'facebook', 'twitter', 'linkedin', 'image')
    
@admin.register(clientsSection)
class ClientsSectionAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'company_url', 'image')

@admin.register(AboutPageSEO)
class AboutPageSEOAdmin(admin.ModelAdmin):
    list_display = ('meta_title', 'meta_description')
    
admin.site.register(teamSectionTitle)