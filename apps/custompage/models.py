from django.db import models
from ckeditor.fields import RichTextField
from apps.lang.models import Languages

class customPage(models.Model):
    title = models.CharField(max_length=100)
    slug = models.CharField(unique=True, blank=True, null=True, max_length=100)
    content = RichTextField()
    language = models.ForeignKey(Languages, on_delete=models.CASCADE, related_name='custom_page_language', blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if self.title:
            original_slug = self.title.replace(" ", "-").replace(",", "").replace(":", "")
            original_slug = original_slug.replace("--", "-")
            queryset = customPage.objects.exclude(pk=self.pk)
            counter = 1

            # Ensure the slug is unique
            while queryset.filter(slug=original_slug).exists():
                original_slug = f"{self.title}-{counter}"
                counter += 1

            self.slug = original_slug.lower()
            
            super().save(*args, **kwargs)
        
    def __str__(self):
        return self.title
    
