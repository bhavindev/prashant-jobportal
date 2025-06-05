from django.contrib import admin
from apps.legals.models import *

# T&C
@admin.register(termsnConditionPage)
class termsnConditionPageAdmin(admin.ModelAdmin):
    list_display = ['terms']

@admin.register(termsnConditionPageSEO)
class termsnConditionPageAdmin(admin.ModelAdmin):
    list_display = ['meta_title', 'meta_description']

# Policy
@admin.register(privacyPolicyPage)
class termsnConditionPageAdmin(admin.ModelAdmin):
    list_display = ['policy']

@admin.register(privacyPolicyPageSEO)
class termsnConditionPageAdmin(admin.ModelAdmin):
    list_display = ['meta_title', 'meta_description']
    
# Agreement
@admin.register(agreement)
class agreementAdmin(admin.ModelAdmin):
    list_display = ['service','client', 'name', 'email', 'is_signed' , 'is_approved']