from django.contrib import admin
from .models import blogs, blogCategory, blogPageSEO

@admin.register(blogs)
class BlogsAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_at', 'thumbnail')

@admin.register(blogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'created_at')

admin.site.register(blogPageSEO)