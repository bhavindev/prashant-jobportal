from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from apps.settings.models import websiteSetting
from apps.lang.models import Languages

class pricing(models.Model):
    title = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, blank=True, null=True)
    price = models.CharField(max_length=255)
    description = RichTextField()
    button_text = models.CharField(max_length=200)
    button_url = models.CharField(max_length=255)
    is_featured = models.BooleanField(default=False)
    featured_badge_title = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    language = models.ForeignKey(Languages, on_delete=models.CASCADE, related_name='pricing_language', blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if self.title:
            original_slug = self.title.replace(" ", "-").replace(",", "").replace(":", "")
            original_slug = original_slug.replace("--", "-")
            queryset = pricing.objects.exclude(pk=self.pk)
            counter = 1

            # Ensure the slug is unique
            while queryset.filter(slug=original_slug).exists():
                original_slug = f"{self.title}-{counter}"
                counter += 1

            self.slug = original_slug.lower()
            
            super().save(*args, **kwargs)
        
    def __str__(self):
        try:
            currency_name = websiteSetting.objects.first().currency_name
        except websiteSetting.DoesNotExist:
            currency_name = "Currency"
            
        return f"{self.title} - {self.price} {currency_name}"

class pricingPageSEO(models.Model):
    meta_title = models.CharField(max_length=200, blank=True, null=True)
    meta_description = models.CharField(max_length=255, blank=True, null=True)
    language = models.ForeignKey(Languages, on_delete=models.CASCADE, related_name='pricing_page_seo_language', blank=True, null=True)
    
    def __str__(self):
        return self.meta_title
    
class pricingSectionTitle(models.Model):
    title_small = models.CharField(max_length=200, blank=True, null=True)
    title_big = models.CharField(max_length=200, blank=True, null=True)
    language = models.ForeignKey(Languages, on_delete=models.CASCADE, related_name='pricing_section_title_language', blank=True, null=True)
    
    def __str__(self):
        return self.title_small

