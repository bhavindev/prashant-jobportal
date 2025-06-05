from django.contrib import admin
from apps.settings.models import *

@admin.register(websiteSetting)
class WebsiteSettingAdmin(admin.ModelAdmin):
    list_display = ['name', 'author', 'email_address']

@admin.register(SeoSetting)
class SeoSettingAdmin(admin.ModelAdmin):
    list_display = ['meta_title', 'meta_description']

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ['name', 'url', 'order']

@admin.register(HeaderFooter)
class HeaderFooterAdmin(admin.ModelAdmin):
    list_display = [
        'footer_col1_subtitle',
        'footer_col1_title',
        'footer_col1_button',
        'footer_col1_button_url',
    ]

admin.site.register(paymentMethod)

admin.site.register(PromotionalBanner)
