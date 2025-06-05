from django.contrib import admin
from apps.contactpage.models import *

@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ['box1_title', 'box2_title', 'box3_title']

@admin.register(contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'message']

@admin.register(ContactPageSEO)
class ContactPageSEOAdmin(admin.ModelAdmin):
    list_display = ['meta_title', 'meta_description']
    
@admin.register(Subscriber)
class ContactPageSEOAdmin(admin.ModelAdmin):
    list_display = ['email', 'subscribe_date']

