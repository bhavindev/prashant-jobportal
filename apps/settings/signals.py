import os
import requests
from django.core.files import File
from django.conf import settings
from django.db import connection
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from apps.lang.models import Languages
from apps.settings.models import *

@receiver(post_migrate)
def create_languages(sender, **kwargs):
    table_name = Languages._meta.db_table
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT EXISTS(SELECT 1 FROM information_schema.tables WHERE table_name = '{table_name}');")
        table_exists = cursor.fetchone()[0]

    if not table_exists:
        print(f"Table {table_name} does not exist. Skipping Languages creation.")
        return

    default_languages = [
        {"name": "English", "code": "en", "is_default": True},
    ]

    for language in default_languages:
        Languages.objects.get_or_create(name=language["name"], defaults=language)
        
        
@receiver(post_migrate)
def create_website_setting(sender, **kwargs):
    if sender.name != 'apps.settings':
        return

    # Check if the websiteSetting table exists
    settings_table_name = websiteSetting._meta.db_table

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT EXISTS (
                SELECT 1 
                FROM information_schema.tables 
                WHERE table_name = %s
            );
        """, [settings_table_name])
        settings_table_exists = cursor.fetchone()[0]

    if not settings_table_exists:
        print(f"Table {settings_table_name} does not exist. Skipping websiteSetting creation.")
        return

    # Get the default language
    try:
        default_language = Languages.objects.get(is_default=True)
    except Languages.DoesNotExist:
        default_language = Languages.objects.create(name="English", code="en", is_default=True)

    # Check if any record exists in websiteSetting
    if not websiteSetting.objects.exists():
        # Image details
        images = {
            "logo_dark": "https://crm.thecodegrammer.net/media/app_config/white.png",
            "logo": "https://crm.thecodegrammer.net/media/app_config/blue.png",
            "invoice_logo": "https://crm.thecodegrammer.net/media/app_config/favicon.jpg",
            "favicon": "https://crm.thecodegrammer.net/media/app_config/favicon.jpg"
        }

        image_paths = {}

        # Download and save images
        for key, url in images.items():
            image_name = os.path.basename(url)
            image_dir = os.path.join(settings.MEDIA_ROOT, 'app_config')
            image_path = os.path.join(image_dir, image_name)

            # Create the directory if it doesn't exist
            if not os.path.exists(image_dir):
                os.makedirs(image_dir)

            # Download the image if it doesn't exist locally
            if not os.path.exists(image_path):
                response = requests.get(url)
                if response.status_code == 200:
                    with open(image_path, 'wb') as f:
                        f.write(response.content)
                    print(f"Image {image_name} downloaded.")
                else:
                    print(f"Failed to download image from {url}")
                    continue

            # Save the local image path to be used in the websiteSetting object creation
            image_paths[key] = image_path

        # Create the websiteSetting entry
        with open(image_paths["logo_dark"], 'rb') as logo_dark_file, \
             open(image_paths["logo"], 'rb') as logo_file, \
             open(image_paths["invoice_logo"], 'rb') as invoice_logo_file, \
             open(image_paths["favicon"], 'rb') as favicon_file:
             
            website_setting_record = websiteSetting.objects.create(
                language=default_language
            )

            # Save the images to their respective fields
            website_setting_record.logo_dark.save(os.path.basename(image_paths["logo_dark"]), File(logo_dark_file))
            website_setting_record.logo.save(os.path.basename(image_paths["logo"]), File(logo_file))
            website_setting_record.invoice_logo.save(os.path.basename(image_paths["invoice_logo"]), File(invoice_logo_file))
            website_setting_record.favicon.save(os.path.basename(image_paths["favicon"]), File(favicon_file))

            print("Website settings created with images.")
    else:
        print("Website settings already exist. Skipping creation.")
        
        
@receiver(post_migrate)
def create_header_footer(sender, **kwargs):
    if sender.name != 'apps.settings':
        return

    # Check if the HeaderFooter table exists
    header_footer_table_name = HeaderFooter._meta.db_table

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT EXISTS (
                SELECT 1 
                FROM information_schema.tables 
                WHERE table_name = %s
            );
        """, [header_footer_table_name])
        header_footer_table_exists = cursor.fetchone()[0]

    if not header_footer_table_exists:
        print(f"Table {header_footer_table_name} does not exist. Skipping HeaderFooter creation.")
        return

    # Get the default language
    try:
        default_language = Languages.objects.get(is_default=True)
    except Languages.DoesNotExist:
        default_language = Languages.objects.create(name="English", code="en", is_default=True)

    # Check if any record exists in HeaderFooter
    if not HeaderFooter.objects.exists():
        HeaderFooter.objects.create(
            footer_col1_subtitle="READY TO DO THIS",
            footer_col1_title="Let's get to work",
            footer_col1_button="Get the offer",
            footer_col1_button_url="/pricing",
            
            footer_col2_title1="Resources",
            footer_col2_description1="""
                <ul>
                    <li><a href="/contact-us/">Contact</a></li>
                    <li><a href="/privacy-policy/">Privacy Policy</a></li>
                    <li><a href="/terms-conditions/">Terms of Use</a></li>
                </ul>
            """,
            
            footer_col2_title2="Support",
            footer_col2_description2="""
                <ul>
                    <li><a href="blog.html">Blog</a></li>
                    <li><a href="case-study.html">Case Studies</a></li>
                    <li><a href="portfolio.html">Portfolio</a></li>
                </ul>
            """,
            
            footer_copyright="© 2021. All rights reserved by The CodeGrammer.",
            project_list_title="Recent Projects",
            footer_small_text="Your design has to be as intuitive as it is helpful and insightful. In the dozen years.",
            
            subscribe_form_title="Get in touch!",
            subscribe_form_description="Subscribe to get exciting offers and our latest news and update for first.",
            subscribe_form_placeholder="Email Address",
            subscribe_form_button="Subscribe",
            
            policy_page_title="Privacy Policy",
            terms_page_title="Terms of Use",
            language=default_language
        )
        print("Header and Footer settings created.")
    else:
        print("Header and Footer settings already exist. Skipping creation.")