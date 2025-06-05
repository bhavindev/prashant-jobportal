from django.db import connection
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from apps.lang.models import Languages
from apps.pricingpage.models import *

@receiver(post_migrate)
def create_arabic_pricing_entries(sender, **kwargs):
    if sender.name != 'apps.pricingpage':
        return

    # Check if the pricing table exists
    pricing_table_name = pricing._meta.db_table

    with connection.cursor() as cursor:
        cursor.execute(f"""
            SELECT EXISTS (
                SELECT 1 
                FROM information_schema.tables 
                WHERE table_name = '{pricing_table_name}'
            );
        """)
        pricing_table_exists = cursor.fetchone()[0]

    if not pricing_table_exists:
        print(f"Table {pricing_table_name} does not exist. Skipping pricing creation.")
        return

    # Get the Arabic language
    try:
        arabic_language = Languages.objects.get(code="ar")
    except Languages.DoesNotExist:
        arabic_language = Languages.objects.create(name="Arabic", code="ar", is_rtl=True)

    # Check if any Arabic pricing entries exist
    if not pricing.objects.filter(language=arabic_language).exists():
        pricing_entries = [
            {
                "title": "احترافي",
                "price": "5000",
                "description": """
                    <ul>
                        <li>10 صفحات لموقع مستجيب</li>
                        <li>5 حملات PPC</li>
                        <li>10 كلمات رئيسية SEO</li>
                        <li>5 حملات فيسبوك</li>
                        <li>2 حملات فيديو</li>
                    </ul>
                """,
                "button_text": "اتصل بنا",
                "button_url": "/contact-us",
                "is_featured": False,
                "featured_badge_title": None,
                "language": arabic_language,
            },
            {
                "title": "قياسي",
                "price": "10000",
                "description": """
                    <ul>
                        <li>50 صفحات لموقع مستجيب</li>
                        <li>10 حملات PPC</li>
                        <li>20 كلمات رئيسية SEO</li>
                        <li>10 حملات فيسبوك</li>
                        <li>4 حملات فيديو</li>
                    </ul>
                """,
                "button_text": "اتصل بنا",
                "button_url": "/contact-us",
                "is_featured": True,
                "featured_badge_title": "شائع",
                "language": arabic_language,
            },
            {
                "title": "نهائي",
                "price": "15000",
                "description": """
                    <ul>
                        <li>30 صفحات لموقع مستجيب</li>
                        <li>15 حملات PPC</li>
                        <li>30 كلمات رئيسية SEO</li>
                        <li>15 حملات فيسبوك</li>
                        <li>6 حملات فيديو</li>
                    </ul>
                """,
                "button_text": "اتصل بنا",
                "button_url": "/contact-us",
                "is_featured": False,
                "featured_badge_title": None,
                "language": arabic_language,
            }
        ]

        # Create Arabic pricing entries
        for entry in pricing_entries:
            pricing.objects.create(
                title=entry["title"],
                price=entry["price"],
                description=entry["description"],
                button_text=entry["button_text"],
                button_url=entry["button_url"],
                is_featured=entry["is_featured"],
                featured_badge_title=entry["featured_badge_title"],
                language=entry["language"],
            )
            print(f"Arabic Pricing plan '{entry['title']}' created.")
    else:
        print("Arabic Pricing entries already exist. Skipping creation.")


@receiver(post_migrate)
def create_arabic_pricing_section_title(sender, **kwargs):
    if sender.name != 'apps.pricingpage':
        return

    # Check if the pricingSectionTitle table exists
    section_title_table_name = pricingSectionTitle._meta.db_table

    with connection.cursor() as cursor:
        cursor.execute(f"""
            SELECT EXISTS (
                SELECT 1 
                FROM information_schema.tables 
                WHERE table_name = '{section_title_table_name}'
            );
        """)
        section_title_table_exists = cursor.fetchone()[0]

    if not section_title_table_exists:
        print(f"Table {section_title_table_name} does not exist. Skipping pricingSectionTitle creation.")
        return

    # Get the Arabic language
    try:
        arabic_language = Languages.objects.get(code="ar")
    except Languages.DoesNotExist:
        arabic_language = Languages.objects.create(name="Arabic", code="ar", is_rtl=True)

    # Check if any Arabic pricingSectionTitle exists
    if not pricingSectionTitle.objects.filter(language=arabic_language).exists():
        pricingSectionTitle.objects.create(
            title_small="أسعارنا",
            title_big="اختر الخطة الأنسب لك",
            language=arabic_language
        )
        print("Arabic Pricing Section Title created.")
    else:
        print("Arabic Pricing Section Title already exists. Skipping creation.")


@receiver(post_migrate)
def create_arabic_pricing_page_seo(sender, **kwargs):
    if sender.name != 'apps.pricingpage':
        return

    # Check if the pricingPageSEO table exists
    seo_table_name = pricingPageSEO._meta.db_table

    with connection.cursor() as cursor:
        cursor.execute(f"""
            SELECT EXISTS (
                SELECT 1 
                FROM information_schema.tables 
                WHERE table_name = '{seo_table_name}'
            );
        """)
        seo_table_exists = cursor.fetchone()[0]

    if not seo_table_exists:
        print(f"Table {seo_table_name} does not exist. Skipping pricingPageSEO creation.")
        return

    # Get the Arabic language
    try:
        arabic_language = Languages.objects.get(code="ar")
    except Languages.DoesNotExist:
        arabic_language = Languages.objects.create(name="Arabic", code="ar", is_rtl=True)

    # Check if any Arabic pricingPageSEO exists
    if not pricingPageSEO.objects.filter(language=arabic_language).exists():
        pricingPageSEO.objects.create(
            meta_title="التسعير",
            meta_description="The CodeGrammer",
            language=arabic_language
        )
        print("Arabic Pricing Page SEO created.")
    else:
        print("Arabic Pricing Page SEO already exists. Skipping creation.")
