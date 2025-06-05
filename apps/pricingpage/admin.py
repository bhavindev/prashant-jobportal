from django.contrib import admin
from apps.pricingpage.models import *

# Register your models here.
@admin.register(pricing)
class pricingAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'button_text', 'button_url', 'is_featured']

@admin.register(pricingPageSEO)
class pricingPageSEOAdmin(admin.ModelAdmin):
    list_display = ['meta_title', 'meta_description']
    
admin.site.register(pricingSectionTitle)