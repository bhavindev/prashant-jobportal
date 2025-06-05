from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from apps.lang.models import Languages

class aboutSettings(models.Model):
    title_white = models.CharField(max_length=200, blank=True, null=True)
    title_red = models.CharField(max_length=200, blank=True, null=True)
    heading = models.CharField(max_length=255, blank=True, null=True)
    description = RichTextField(blank=True, null=True)
    count_title1 = models.CharField(max_length=255, blank=True, null=True)
    years_of_experience = models.IntegerField(blank=True, null=True)
    count_title2 = models.CharField(max_length=255, blank=True, null=True)
    project_delivered = models.IntegerField(blank=True, null=True)
    button_text = models.CharField(max_length=255, blank=True, null=True)
    button_url = models.CharField(max_length=255, blank=True, null=True)
    language = models.ForeignKey(Languages, on_delete=models.CASCADE, related_name='about_language', blank=True, null=True)
    
    def __str__(self):
        return self.title_white 
    
    class Meta:
        verbose_name_plural = "1. About Page Intro"
    

class teamSection(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    about = models.TextField(blank=True, null=True)
    slug = models.CharField(max_length=200, blank=True, null=True)
    position = models.CharField(max_length=200, blank=True, null=True)
    facebook = models.CharField(max_length=255, default="https://www.facebook.com", blank=True, null=True)
    twitter = models.CharField(max_length=255, default="https://twitter.com", blank=True, null=True)
    linkedin = models.CharField(max_length=255, default="https://www.linkedin.com", blank=True, null=True)
    image = models.ImageField(upload_to='team/', blank=True, null=True)
    language = models.ForeignKey(Languages, on_delete=models.CASCADE, related_name='team_language', blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if self.name:
            original_slug = self.name.replace(" ", "-").replace(",", "").replace(":", "")
            original_slug = original_slug.replace("--", "-")
            queryset = teamSection.objects.exclude(pk=self.pk)
            counter = 1

            # Ensure the slug is unique
            while queryset.filter(slug=original_slug).exists():
                original_slug = f"{self.name}-{counter}"
                counter += 1

            self.slug = original_slug.lower()
            
            super().save(*args, **kwargs)
        
    def __str__(self):
        return self.name
    
    def get_image(self):
        image = self.image.url
        return image
    
    class Meta:
        verbose_name_plural = "2. Team Members"
        
class teamSectionTitle(models.Model):
    title_small = models.CharField(max_length=200, blank=True, null=True)
    title_big = models.CharField(max_length=200, blank=True, null=True)
    language = models.ForeignKey(Languages, on_delete=models.CASCADE, related_name='team_title_language', blank=True, null=True)
    
    def __str__(self):
        return self.title_small

class clientsSection(models.Model):
    company_name = models.CharField(max_length=200, blank=True, null=True)
    slug = models.CharField(max_length=200, blank=True, null=True)
    company_url = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to='clients/')
    language = models.ForeignKey(Languages, on_delete=models.CASCADE, related_name='clients_language', blank=True, null=True)
        
    def save(self, *args, **kwargs):
        if self.company_name:
            original_slug = self.company_name.replace(" ", "-").replace(",", "").replace(":", "")
            original_slug = original_slug.replace("--", "-")
            queryset = clientsSection.objects.exclude(pk=self.pk)
            counter = 1

            # Ensure the slug is unique
            while queryset.filter(slug=original_slug).exists():
                original_slug = f"{self.company_name}-{counter}"
                counter += 1

            self.slug = original_slug.lower()
            
            super().save(*args, **kwargs)
    
    def __str__(self):
        return self.company_name
    
    class Meta:
        verbose_name_plural = "3. Clients"
    
class AboutPageSEO(models.Model):
    meta_title = models.CharField(max_length=255, blank=True, null=True)
    meta_description = models.CharField(max_length=255, blank=True, null=True)
    language = models.ForeignKey(Languages, on_delete=models.CASCADE, related_name='about_seo_language', blank=True, null=True)
