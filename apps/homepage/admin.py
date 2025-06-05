from django.contrib import admin
from apps.homepage.models import *

@admin.register(bannerSection)
class bannerSectionAdmin(admin.ModelAdmin):
    list_display = ['title']

@admin.register(serviceSection)
class ServiceSectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'description']

@admin.register(projectsSection)
class ProjectsSectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'category']


@admin.register(projectCategory)
class ProjectCategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']

@admin.register(funFactSection)
class FunFactSectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'fact_count']


@admin.register(testimonialsSection)
class TestimonialsSectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'client_name', 'client_designation']
    
@admin.register(HomePageSEO)
class HomePageSEOAdmin(admin.ModelAdmin):
    list_display = ['meta_title', 'meta_description']
    
admin.site.register(serviceSectionTitle)
admin.site.register(clientSectionTitle)
admin.site.register(projectSectionTitle)
admin.site.register(testimonialSectionTitle)
admin.site.register(blogSectionTitle)
admin.site.register(funFactSectionTitle)