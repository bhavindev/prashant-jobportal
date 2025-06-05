from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from apps.lang.models import Languages

class bannerSection(models.Model):
    background_image = models.ImageField(upload_to='Home_images/', blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    button_text = models.CharField(max_length=200, blank=True, null=True)
    button_url = models.CharField(max_length=255, blank=True, null=True)
    show_quote_form = models.BooleanField(default=True)
    quote_form_title = models.CharField(max_length=200, blank=True, null=True)
    
    quote_form_field1_title = models.CharField(max_length=200, blank=True, null=True)
    quote_form_field1_placeholder = models.CharField(max_length=200, blank=True, null=True)
    
    quote_form_field2_title = models.CharField(max_length=200, blank=True, null=True)
    quote_form_field2_placeholder = models.CharField(max_length=200, blank=True, null=True)
    
    quote_form_field3_title = models.CharField(max_length=200, blank=True, null=True)
    quote_form_field3_placeholder = models.CharField(max_length=200, blank=True, null=True)
    
    quote_form_button_text = models.CharField(max_length=200, blank=True, null=True)
    
    language = models.ForeignKey(Languages, on_delete=models.CASCADE, related_name='banner_language', blank=True, null=True)

    def __str__(self):
        return self.title
    
class serviceSection(models.Model):
    image = models.ImageField(upload_to='Home_images/')
    title = models.CharField(max_length=200)
    slug = models.CharField(max_length=220, blank=True, null=True)
    description = RichTextField(blank=True, null=True)
    order = models.IntegerField(default=0)
    language = models.ForeignKey(Languages, on_delete=models.CASCADE, related_name='service_language', blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if self.title:
            original_slug = self.title.replace(" ", "-").replace(",", "").replace(":", "").replace("/", "")
            original_slug = original_slug.replace("--", "-")
            queryset = serviceSection.objects.exclude(pk=self.pk)
            counter = 1

            # Ensure the slug is unique
            while queryset.filter(slug=original_slug).exists():
                original_slug = f"{self.title}-{counter}"
                counter += 1

            self.slug = original_slug.lower()
            
            super().save(*args, **kwargs)
    
    class Meta:
        verbose_name_plural = "2. Services"
    
class projectsSection(models.Model):
    image = models.ImageField(upload_to='Home_images/')
    title = models.CharField(max_length=200, blank=True, null=True)
    slug = models.CharField(null=True, blank=True, max_length=255)
    category = models.ForeignKey('projectCategory',on_delete=models.CASCADE, related_name='prject_category')
    description = RichTextField(blank=True, null=True)
    client = models.CharField(max_length=255, blank=True, null=True)
    duration = models.CharField(max_length=255, blank=True, null=True)
    button_text = models.CharField(max_length=200, blank=True, null=True)
    button_url = models.CharField(max_length=255, blank=True, null=True)
    order = models.IntegerField(default=0)
    language = models.ForeignKey(Languages, on_delete=models.CASCADE, related_name='project_language', blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if self.title:
            original_slug = self.title.replace(" ", "-").replace(",", "").replace(":", "").replace("/", "")
            original_slug = original_slug.replace("--", "-")
            queryset = projectsSection.objects.exclude(pk=self.pk)
            counter = 1

            # Ensure the slug is unique
            while queryset.filter(slug=original_slug).exists():
                original_slug = f"{self.title}-{counter}"
                counter += 1

            self.slug = original_slug.lower()
            
            super().save(*args, **kwargs)
    
    class Meta:
        verbose_name_plural = "3. Projects"
        
class projectCategory(models.Model):
    title = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, null=True, blank=True)
    language = models.ForeignKey(Languages, on_delete=models.CASCADE, related_name='project_category_language', blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.title:
            original_slug = self.title.replace(" ", "-").replace(",", "").replace(":", "").replace("/", "")
            original_slug = original_slug.replace("--", "-")
            queryset = projectCategory.objects.exclude(pk=self.pk)
            counter = 1

            # Ensure the slug is unique
            while queryset.filter(slug=original_slug).exists():
                original_slug = f"{self.title}-{counter}"
                counter += 1

            self.slug = original_slug.lower()
            
            super().save(*args, **kwargs)
        
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = "4. Project Categories"

class funFactSection(models.Model):
    fact_count = models.CharField(max_length=100, blank=True, null=True)
    title = models.CharField(max_length=200, blank=True, null=True)
    slug = models.CharField(max_length=255, null=True, blank=True)
    language = models.ForeignKey(Languages, on_delete=models.CASCADE, related_name='funfact_language', blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if self.title:
            original_slug = self.title.replace(" ", "-").replace(",", "").replace(":", "")
            original_slug = original_slug.replace("--", "-")
            queryset = funFactSection.objects.exclude(pk=self.pk)
            counter = 1

            # Ensure the slug is unique
            while queryset.filter(slug=original_slug).exists():
                original_slug = f"{self.title}-{counter}"
                counter += 1

            self.slug = original_slug.lower()
            
            super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = "5. Fun Facts"

class testimonialsSection(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True)
    slug = models.CharField(max_length=255, null=True, blank=True)
    client_name = models.CharField(max_length=255, blank=True, null=True)
    client_designation = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    language = models.ForeignKey(Languages, on_delete=models.CASCADE, related_name='testimonial_language', blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if self.title:
            original_slug = self.title.replace(" ", "-").replace(",", "").replace(":", "")
            original_slug = original_slug.replace("--", "-")
            queryset = testimonialsSection.objects.exclude(pk=self.pk)
            counter = 1

            # Ensure the slug is unique
            while queryset.filter(slug=original_slug).exists():
                original_slug = f"{self.title}-{counter}"
                counter += 1

            self.slug = original_slug.lower()
            
            super().save(*args, **kwargs)
    
    class Meta:
        verbose_name_plural = "6. Testimonials"
        
class clientSectionTitle(models.Model):
    title_small = models.CharField(max_length=200, blank=True, null=True)
    title_big = models.CharField(max_length=255, blank=True, null=True)
    language = models.ForeignKey(Languages, on_delete=models.CASCADE, related_name='client_title_language', blank=True, null=True)
    
    def __str__(self):
        return self.title_small
    
class testimonialSectionTitle(models.Model):
    title_small = models.CharField(max_length=200, blank=True, null=True)
    title_big = models.CharField(max_length=255, blank=True, null=True)
    language = models.ForeignKey(Languages, on_delete=models.CASCADE, related_name='testimonial_title_language', blank=True, null=True)
    
    def __str__(self):
        return self.title_small
    
class projectSectionTitle(models.Model):
    title_small = models.CharField(max_length=200, blank=True, null=True)
    title_big = models.CharField(max_length=255, blank=True, null=True)
    all_work_text = models.CharField(max_length=200, blank=True, null=True)
    language = models.ForeignKey(Languages, on_delete=models.CASCADE, related_name='project_title_language', blank=True, null=True)
    
    def __str__(self):
        return self.title_small
    
class serviceSectionTitle(models.Model):
    title_small = models.CharField(max_length=200, blank=True, null=True)
    title_big = models.CharField(max_length=255, blank=True, null=True)
    service_card_more_text = models.CharField(max_length=200, blank=True, null=True)
    language = models.ForeignKey(Languages, on_delete=models.CASCADE, related_name='service_title_language', blank=True, null=True)
    
    def __str__(self):
        return self.title_small
    
class funFactSectionTitle(models.Model):
    title_small = models.CharField(max_length=200, blank=True, null=True)
    title_big = models.CharField(max_length=255, blank=True, null=True)
    language = models.ForeignKey(Languages, on_delete=models.CASCADE, related_name='funfact_title_language', blank=True, null=True)
    
    def __str__(self):
        return self.title_small
    
class blogSectionTitle(models.Model):
    title_small = models.CharField(max_length=200, blank=True, null=True)
    title_big = models.CharField(max_length=255, blank=True, null=True)
    language = models.ForeignKey(Languages, on_delete=models.CASCADE, related_name='blog_title_language', blank=True, null=True)
    
    def __str__(self):
        return self.title_small

class HomePageSEO(models.Model):
    meta_title = models.CharField(max_length=255, blank=True, null=True)
    meta_description = models.CharField(max_length=255, blank=True, null=True)
    language = models.ForeignKey(Languages, on_delete=models.CASCADE, related_name='home_seo_language', blank=True, null=True)

    

    