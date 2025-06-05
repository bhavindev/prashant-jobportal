from django.db import models
from ckeditor.fields import RichTextField
from apps.lang.models import Languages

class ContactInfo(models.Model):
    box1_icon = models.CharField(max_length=255, blank=True, null=True)
    box1_title = models.CharField(max_length=250, blank=True, null=True)
    box1_description = RichTextField(blank=True, null=True)
    
    box2_icon = models.CharField(max_length=255, blank=True, null=True)
    box2_title = models.CharField(max_length=250, blank=True, null=True)
    box2_description = RichTextField(blank=True, null=True)
    
    box3_icon = models.CharField(max_length=255, blank=True, null=True)
    box3_title = models.CharField(max_length=250, blank=True, null=True)
    box3_description = RichTextField(blank=True, null=True)
    
    iframe_title = models.CharField(max_length=200, blank=True, null=True)
    map_iframe = models.TextField(blank=True, null=True)
    
    form_title = models.CharField(max_length=200, blank=True, null=True)
    
    name_field_label = models.CharField(max_length=200, blank=True, null=True)
    name_field_placeholder = models.CharField(max_length=200, blank=True, null=True)
    
    email_field_label = models.CharField(max_length=200, blank=True, null=True)
    email_field_placeholder = models.CharField(max_length=200, blank=True, null=True)
    
    phone_field_label = models.CharField(max_length=200, blank=True, null=True)
    phone_field_placeholder = models.CharField(max_length=200, blank=True, null=True)
    
    message_field_label = models.CharField(max_length=200, blank=True, null=True)
    message_field_placeholder = models.CharField(max_length=200, blank=True, null=True)
    
    upload_field_label = models.CharField(max_length=200, blank=True, null=True)
    
    submit_button_text = models.CharField(max_length=200, blank=True, null=True)
    
    language = models.ForeignKey(Languages, on_delete=models.CASCADE, related_name='contact_info_language', blank=True, null=True)

class contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=500)
    phone = models.IntegerField()
    message = models.TextField(blank=True)
    uploaded_file = models.FileField(upload_to='contact_files', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
class ContactPageSEO(models.Model):
    meta_title = models.CharField(max_length=255, blank=True, null=True)
    meta_description = models.CharField(max_length=255, blank=True, null=True)
    language = models.ForeignKey(Languages, on_delete=models.CASCADE, related_name='contact_page_seo_language', blank=True, null=True)

class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribe_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.email