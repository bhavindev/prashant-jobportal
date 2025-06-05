from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from apps.authapp.models import UserProfile
from apps.lang.models import Languages
from unidecode import unidecode

class blogs(models.Model):
    thumbnail = models.ImageField(upload_to='blogs')
    title = models.CharField(max_length=255)
    category = models.ForeignKey('blogCategory', on_delete=models.SET_NULL, null=True)
    slug = models.CharField(max_length=255, blank=True, null=True)
    description = RichTextField()
    author = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    language = models.ForeignKey(Languages, on_delete=models.CASCADE, related_name='blog_language', blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if self.title:
            original_slug = self.title.replace(" ", "-").replace(",", "").replace(":", "")
            original_slug = original_slug.replace("--", "-")
            queryset = blogs.objects.exclude(pk=self.pk)
            counter = 1

            # Ensure the slug is unique
            while queryset.filter(slug=original_slug).exists():
                original_slug = f"{self.title}-{counter}"
                counter += 1

            self.slug = original_slug.lower()
            
            super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    
class blogCategory(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True, null=True, max_length=100)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    language = models.ForeignKey(Languages, on_delete=models.CASCADE, related_name='blog_category_language', blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if self.title:
            original_slug = self.title.replace(" ", "-").replace(",", "").replace(":", "")
            original_slug = original_slug.replace("--", "-")
            queryset = blogCategory.objects.exclude(pk=self.pk)
            counter = 1

            # Ensure the slug is unique
            while queryset.filter(slug=original_slug).exists():
                original_slug = f"{self.title}-{counter}"
                counter += 1

            self.slug = original_slug.lower()
            
            super().save(*args, **kwargs)
        
    def __str__(self):
        return self.title
    
class blogPageSEO(models.Model):
    meta_title = models.CharField(max_length=200, blank=True, null=True)
    meta_description = models.CharField(max_length=255, blank=True, null=True)
    language = models.ForeignKey(Languages, on_delete=models.CASCADE, related_name='blog_page_seo_language', blank=True, null=True)
    
    def __str__(self):
        return self.meta_title
    
