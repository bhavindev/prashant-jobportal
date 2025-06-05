from django.db import models
from apps.lang.models import Languages

class ServicePageSEO(models.Model):
    meta_title = models.CharField(max_length=255, blank=True, null=True)
    meta_description = models.CharField(max_length=255, blank=True, null=True)
    language = models.ForeignKey(Languages, on_delete=models.CASCADE, related_name='service_page_seo_language', blank=True, null=True)