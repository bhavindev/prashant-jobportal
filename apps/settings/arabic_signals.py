from django.db import connection
from django.conf import settings
from django.core.files import File
import os
import requests
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from apps.lang.models import Languages
from apps.settings.models import websiteSetting, HeaderFooter


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
        {"name": "Arabic", "code": "ar", "is_rtl": True},
    ]

    for language in default_languages:
        Languages.objects.get_or_create(code=language["code"], defaults=language)
    print("Languages created or already exist.")


@receiver(post_migrate)
def create_website_setting(sender, **kwargs):
    if sender.name != 'apps.settings':
        return

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

    try:
        arabic_language = Languages.objects.get(code="ar")
    except Languages.DoesNotExist:
        arabic_language = Languages.objects.create(name="Arabic", code="ar", is_rtl=True)

    if not websiteSetting.objects.filter(language=arabic_language).exists():
        images = {
            "logo_dark": "https://crm.thecodegrammer.net/media/app_config/white.png",
            "logo": "https://crm.thecodegrammer.net/media/app_config/blue.png",
            "invoice_logo": "https://crm.thecodegrammer.net/media/app_config/favicon.jpg",
            "favicon": "https://crm.thecodegrammer.net/media/app_config/favicon.jpg"
        }

        image_paths = {}
        for key, url in images.items():
            image_name = os.path.basename(url)
            image_dir = os.path.join(settings.MEDIA_ROOT, 'app_config')
            image_path = os.path.join(image_dir, image_name)

            if not os.path.exists(image_dir):
                os.makedirs(image_dir)

            if not os.path.exists(image_path):
                response = requests.get(url)
                if response.status_code == 200:
                    with open(image_path, 'wb') as f:
                        f.write(response.content)
                    print(f"Image {image_name} downloaded.")
                else:
                    print(f"Failed to download image from {url}")
                    continue

            image_paths[key] = image_path

        with open(image_paths["logo_dark"], 'rb') as logo_dark_file, \
             open(image_paths["logo"], 'rb') as logo_file, \
             open(image_paths["invoice_logo"], 'rb') as invoice_logo_file, \
             open(image_paths["favicon"], 'rb') as favicon_file:
             
            website_setting_record = websiteSetting.objects.create(
                language=arabic_language
            )

            website_setting_record.logo_dark.save(os.path.basename(image_paths["logo_dark"]), File(logo_dark_file))
            website_setting_record.logo.save(os.path.basename(image_paths["logo"]), File(logo_file))
            website_setting_record.invoice_logo.save(os.path.basename(image_paths["invoice_logo"]), File(invoice_logo_file))
            website_setting_record.favicon.save(os.path.basename(image_paths["favicon"]), File(favicon_file))

            print("Arabic Website settings created with images.")
    else:
        print("Arabic Website settings already exist. Skipping creation.")


@receiver(post_migrate)
def create_header_footer(sender, **kwargs):
    if sender.name != 'apps.settings':
        return

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

    try:
        arabic_language = Languages.objects.get(code="ar")
    except Languages.DoesNotExist:
        arabic_language = Languages.objects.create(name="Arabic", code="ar", is_rtl=True)

    if not HeaderFooter.objects.filter(language=arabic_language).exists():
        HeaderFooter.objects.create(
            footer_col1_subtitle="جاهز للقيام بذلك",
            footer_col1_title="لنبدأ العمل",
            footer_col1_button="احصل على العرض",
            footer_col1_button_url="/pricing",
            
            footer_col2_title1="الموارد",
            footer_col2_description1="""
                <ul>
                    <li><a href="/contact-us/">الاتصال</a></li>
                    <li><a href="/privacy-policy/">سياسة الخصوصية</a></li>
                    <li><a href="/terms-conditions/">شروط الاستخدام</a></li>
                </ul>
            """,
            
            footer_col2_title2="الدعم",
            footer_col2_description2="""
                <ul>
                    <li><a href="blog.html">المدونة</a></li>
                    <li><a href="case-study.html">دراسات الحالة</a></li>
                    <li><a href="portfolio.html">المحفظة</a></li>
                </ul>
            """,
            
            footer_copyright="© 2021. جميع الحقوق محفوظة لشركة The CodeGrammer.",
            project_list_title="المشاريع الأخيرة",
            footer_small_text="يجب أن يكون تصميمك بديهيًا كما هو مفيد وبديهي.",
            
            subscribe_form_title="ابقى على تواصل!",
            subscribe_form_description="اشترك للحصول على عروض مثيرة وأحدث أخبارنا وتحديثاتنا.",
            subscribe_form_placeholder="عنوان البريد الإلكتروني",
            subscribe_form_button="اشترك",
            
            policy_page_title="سياسة الخصوصية",
            terms_page_title="شروط الاستخدام",
            language=arabic_language
        )
        print("Arabic Header and Footer settings created.")
    else:
        print("Arabic Header and Footer settings already exist. Skipping creation.")