from django.db import models
from ckeditor.fields import RichTextField
from django.utils.text import slugify
from apps.lang.models import Languages

class websiteSetting(models.Model):
    name = models.CharField(max_length=255, default='Application Name')
    logo_dark = models.ImageField(upload_to='app_config/', blank=True, null=True)
    logo = models.ImageField(upload_to='app_config/', blank=True, null=True)
    logo_width = models.IntegerField(blank=True, null=True)
    invoice_logo = models.ImageField(upload_to='app_config', blank=True, null=True)
    invoice_logo_width = models.IntegerField(blank=True, null=True)
    favicon = models.ImageField(upload_to='app_config/', blank=True, null=True)
    
    author = models.CharField(max_length=200, default='Author Name', blank=True, null=True)
    email_address = models.EmailField(max_length=500, default='test@gmail.com', blank=True, null=True)
    phone_or_whatsapp = models.CharField(max_length=20, default='88012454784', blank=True, null=True)
    price_ragne = models.CharField(max_length=50, default='60$ to 7000$', blank=True, null=True)
    country = models.CharField(max_length=255, default='Your Country', blank=True, null=True)
    address = models.CharField(max_length=255, default='Your Address', blank=True, null=True)
    state = models.CharField(max_length=200, default='Your State', blank=True, null=True)
    Zip = models.CharField(default=12345, max_length=10, blank=True, null=True)
    
    analytics_code = models.CharField(max_length=255, blank=True, null=True, default="GA_MEASUREMENT_ID")
    facebook_pixel_code = models.TextField(blank=True, null=True)
    facebook_chat_code = models.TextField(blank=True, null=True)
    whatsapp_is_active = models.BooleanField(default=True)
    messenger_is_active = models.BooleanField(default=True)
    default_menu_is_active = models.BooleanField(default=True)
    
    currency_name = models.CharField(max_length=100, default='USD')
    currency_symbol = models.CharField(max_length=150, default='$')
    
    twilio_sid = models.CharField(max_length=255, blank=True, null=True)
    twilio_auth_token = models.CharField(max_length=255, blank=True, null=True)
    twilio_from_number = models.CharField(max_length=15, blank=True, null=True)
    
    openai_api = models.CharField(max_length=255, blank=True, null=True)
    max_token = models.IntegerField(default=150, blank=True, null=True)
    is_enabled_for_user = models.BooleanField(default=False)
    
    is_purchasing_enable = models.BooleanField(default=True)
    is_auto_invoice_enable = models.BooleanField(default=True)
    
    hrm_attendance_clock_in_max_time = models.TimeField(blank=True, null=True)
    hrm_attendance_clock_out_min_time = models.TimeField(blank=True, null=True)
    
    DIRECTION_CHOICES = (
        ('Left', 'Left'),
        ('Right', 'Right'),
    )
    whatsapp_button_direction = models.CharField(max_length=10, choices=DIRECTION_CHOICES, default='Right')
    scroll_to_top_direction = models.CharField(max_length=10, choices=DIRECTION_CHOICES, default='Left')
    
    primary_color = models.CharField(max_length=100, default='#5956E9', blank=True, null=True)
    link_color = models.CharField(max_length=100, default='#2522BA', blank=True, null=True)
    wp_button_shed_color = models.CharField(max_length=100, default='#6487ff', blank=True, null=True)
    COLOR_MODE_CHOICES = (
        ('Light', 'Light'),
        ('Dark', 'Dark'),
    )
    default_mode = models.CharField(max_length=10, choices=COLOR_MODE_CHOICES, default='Dark')
    
    is_search_active = models.BooleanField(default=True)
    
    custom_css = models.TextField(blank=True, null=True)
    custom_js = models.TextField(blank=True, null=True)
    
    language = models.ForeignKey(Languages, on_delete=models.CASCADE, related_name='website_language', blank=True, null=True)
    
class SeoSetting(models.Model):
    meta_title = models.CharField(max_length=255, default="Meta Title", blank=True, null=True)
    tag_line = models.CharField(max_length=255, default="Tagline", blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True, default="Meta Description")
    seo_keywords = models.TextField(default='software,application,marketer,developer', blank=True, null=True)
    meta_image = models.ImageField(upload_to='app_config/', blank=True, null=True)
    language = models.ForeignKey(Languages, on_delete=models.CASCADE, related_name='seo_language', blank=True, null=True)

    def __str__(self):
        return 'SEO Setting Configs'

class Menu(models.Model):
    name = models.CharField(max_length=200)
    slug = models.CharField(max_length=200, null=True, blank=True)
    url = models.CharField(max_length=255)
    order = models.IntegerField()
    language = models.ForeignKey(Languages, on_delete=models.CASCADE, related_name='menu_language', blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if self.name:
            original_slug = self.name.replace(" ", "-").replace(",", "").replace(":", "")
            original_slug = original_slug.replace("--", "-")
            queryset = Menu.objects.exclude(pk=self.pk)
            counter = 1

            # Ensure the slug is unique
            while queryset.filter(slug=original_slug).exists():
                original_slug = f"{self.name}-{counter}"
                counter += 1

            self.slug = original_slug
            
            super().save(*args, **kwargs)
    
class HeaderFooter(models.Model):
    
    LAYOUT_CHOICE = (
        ('1', 'Layout 1'),
        ('2', 'Layout 2'),
    )
    footer_layout = models.CharField(max_length=10, choices=LAYOUT_CHOICE, default='1')
    footer_col1_subtitle = models.CharField(max_length=255, blank=True, null=True)  
    footer_col1_title = models.CharField(max_length=255, blank=True, null=True)
    footer_col1_button = models.CharField(max_length=255, blank=True, null=True)
    footer_col1_button_url = models.CharField(max_length=255, blank=True, null=True)
    
    facebook = models.CharField(max_length=255, blank=True, null=True, default="https://facebook.com")
    instagram = models.CharField(max_length=255, blank=True, null=True, default="https://instagram.com")
    twitter = models.CharField(max_length=255, blank=True, null=True, default="https://twitter.com")
    linkedin = models.CharField(max_length=255, blank=True, null=True, default="https://linkedin.com")
    youtube = models.CharField(max_length=255, blank=True, null=True, default="https://youtube.com")
    pinterest = models.CharField(max_length=255, blank=True, null=True, default="https://pinterest.com")
    
    footer_col2_title1 = models.CharField(max_length=255, blank=True, null=True)
    footer_col2_description1 = RichTextField(blank=True, null=True)
    
    footer_col2_title2 = models.CharField(max_length=255, blank=True, null=True)
    footer_col2_description2 = RichTextField(blank=True, null=True)
    
    footer_copyright = models.CharField(max_length=255, blank=True, null=True)
    
    project_list_title = models.CharField(max_length=100, blank=True, null=True)
    LIST_CHOICES = (
        ('Services', 'Services'),
        ('Projects', 'Projects'),
    )
    what_to_show = models.CharField(max_length=10, choices=LIST_CHOICES, default='Projects')
    footer_small_text = models.TextField(blank=True, null=True)
    subscribe_form_title = models.CharField(max_length=100, blank=True, null=True)
    subscribe_form_description = models.CharField(max_length=200, blank=True, null=True)
    subscribe_form_placeholder = models.CharField(max_length=100, blank=True, null=True)
    subscribe_form_button = models.CharField(max_length=100, blank=True, null=True)
    
    policy_page_title = models.CharField(max_length=100, blank=True, null=True)
    terms_page_title = models.CharField(max_length=100, blank=True, null=True)
    
    language = models.ForeignKey(Languages, on_delete=models.CASCADE, related_name='header_footer_language', blank=True, null=True)
    
class paymentMethod(models.Model):
    # SSL Commerze
    ssl_commerze_store_id = models.CharField(max_length=255, blank=True, null=True)
    ssl_commerze_store_pass = models.CharField(max_length=255, blank=True, null=True)
    ssl_commerze_is_sandbox = models.BooleanField(default=False)
    ssl_commerze_is_active = models.BooleanField(default=False)
    
    # PayPal
    paypal_client_id = models.CharField(max_length=255, blank=True, null=True)
    paypal_client_secret = models.CharField(max_length=255, blank=True, null=True)
    paypal_is_sandbox = models.BooleanField(default=False)
    paypal_is_active = models.BooleanField(default=False)
    
    # Stripe
    stripe_publish_key = models.CharField(max_length=255, blank=True, null=True)
    stripe_secret_key = models.CharField(max_length=255, blank=True, null=True)
    stripe_is_sandbox = models.BooleanField(default=False)
    stripe_is_active = models.BooleanField(default=False)
    
    # Stripe
    instamojo_api_key = models.CharField(max_length=255, blank=True, null=True)
    instamojo_auth_token = models.CharField(max_length=255, blank=True, null=True)
    instamojo_is_sandbox = models.BooleanField(default=False)
    instamojo_is_active = models.BooleanField(default=False)
    
    # Razorpay
    razorpay_api_key = models.CharField(max_length=255, blank=True, null=True)
    razorpay_api_secret = models.CharField(max_length=255, blank=True, null=True)
    razorpay_is_active = models.BooleanField(default=False)
    
    # Paymob
    paymob_secret_key = models.CharField(max_length=255, blank=True, null=True)
    paymob_public_key = models.CharField(max_length=255, blank=True, null=True)
    paymob_integration_id = models.IntegerField(blank=True, null=True)
    paymob_is_sandbox = models.BooleanField(default=False)
    paymob_is_active = models.BooleanField(default=False)
    
    # Offline Payment
    offline_payment_instruction = RichTextField(blank=True, null=True)
    offline_payment_is_active = models.BooleanField(default=False)
    
    def __str__(self):
        return f'Payment Methods'
    
#==== Promotional Banner ====#
class PromotionalBanner(models.Model):
    promo_text = RichTextField(blank=True, null=True, default="🎉 Enjoy $5000 discount on all products! Use code: <strong>WELCOME50</strong>")
    promo_url = models.CharField(max_length=255, blank=True, null=True, default="#")
    promo_start_date = models.DateField(blank=True, null=True)
    promo_end_date = models.DateField(blank=True, null=True)
    is_promo_active = models.BooleanField(default=False)
    language = models.ForeignKey(Languages, on_delete=models.CASCADE, related_name='promo_language', blank=True, null=True)
    
    def __str__(self):
        return f'Promotional Banner'