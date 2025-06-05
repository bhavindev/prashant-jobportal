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
def create_bangla_language(sender, **kwargs):
    table_name = Languages._meta.db_table
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT EXISTS(SELECT 1 FROM information_schema.tables WHERE table_name = '{table_name}');")
        table_exists = cursor.fetchone()[0]

    if not table_exists:
        print(f"Table {table_name} does not exist. Skipping Languages creation.")
        return

    # Create Bangla language if it doesn't exist
    default_languages = [
        {"name": "English", "code": "en", "is_default": True},
        {"name": "Bangla", "code": "bn", "is_default": False, "is_rtl": False}
    ]

    for language in default_languages:
        Languages.objects.get_or_create(name=language["name"], defaults=language)
    print("Languages created/updated.")


@receiver(post_migrate)
def create_bangla_website_setting(sender, **kwargs):
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

    # Get the Bangla language
    try:
        bangla_language = Languages.objects.get(code="bn")
    except Languages.DoesNotExist:
        bangla_language = Languages.objects.create(name="Bangla", code="bn", is_rtl=False)

    # Check if any record exists in websiteSetting
    if not websiteSetting.objects.filter(language=bangla_language).exists():
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
                language=bangla_language
            )

            # Save the images to their respective fields
            website_setting_record.logo_dark.save(os.path.basename(image_paths["logo_dark"]), File(logo_dark_file))
            website_setting_record.logo.save(os.path.basename(image_paths["logo"]), File(logo_file))
            website_setting_record.invoice_logo.save(os.path.basename(image_paths["invoice_logo"]), File(invoice_logo_file))
            website_setting_record.favicon.save(os.path.basename(image_paths["favicon"]), File(favicon_file))

            print("Bangla Website settings created with images.")
    else:
        print("Bangla Website settings already exist. Skipping creation.")


@receiver(post_migrate)
def create_bangla_header_footer(sender, **kwargs):
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

    # Get the Bangla language
    try:
        bangla_language = Languages.objects.get(code="bn")
    except Languages.DoesNotExist:
        bangla_language = Languages.objects.create(name="Bangla", code="bn", is_rtl=False)

    # Check if any record exists in HeaderFooter
    if not HeaderFooter.objects.filter(language=bangla_language).exists():
        HeaderFooter.objects.create(
            footer_col1_subtitle="প্রস্তুত আছেন কি?",
            footer_col1_title="চলুন কাজ শুরু করি",
            footer_col1_button="অফার পান",
            footer_col1_button_url="/pricing",
            
            footer_col2_title1="রিসোর্স",
            footer_col2_description1="""
                <ul>
                    <li><a href="/contact-us/">যোগাযোগ করুন</a></li>
                    <li><a href="/privacy-policy/">গোপনীয়তা নীতি</a></li>
                    <li><a href="/terms-conditions/">ব্যবহারের শর্তাবলী</a></li>
                </ul>
            """,
            
            footer_col2_title2="সহায়তা",
            footer_col2_description2="""
                <ul>
                    <li><a href="blog.html">ব্লগ</a></li>
                    <li><a href="case-study.html">কেস স্টাডি</a></li>
                    <li><a href="portfolio.html">পোর্টফোলিও</a></li>
                </ul>
            """,
            
            footer_copyright="© 2021. সমস্ত অধিকার সংরক্ষিত দ্য কোডগ্রামারের দ্বারা।",
            project_list_title="সাম্প্রতিক প্রকল্পসমূহ",
            footer_small_text="আপনার ডিজাইনটি যতটা অন্তর্দৃষ্টিপূর্ণ ততটা স্বজ্ঞাত হতে হবে। গত এক দশকে আমরা ডিজাইন ও ডেভেলপমেন্টে এক অসাধারণ স্তরে পৌঁছেছি।",
            
            subscribe_form_title="যোগাযোগে থাকুন!",
            subscribe_form_description="আমাদের উত্তেজনাপূর্ণ অফার এবং সর্বশেষ সংবাদ ও আপডেট সম্পর্কে জানতে সাবস্ক্রাইব করুন।",
            subscribe_form_placeholder="ইমেইল ঠিকানা",
            subscribe_form_button="সাবস্ক্রাইব করুন",
            
            policy_page_title="গোপনীয়তা নীতি",
            terms_page_title="ব্যবহারের শর্তাবলী",
            language=bangla_language
        )
        print("Bangla Header and Footer settings created.")
    else:
        print("Bangla Header and Footer settings already exist. Skipping creation.")