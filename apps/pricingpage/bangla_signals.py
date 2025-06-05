from django.db import connection
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from apps.lang.models import Languages
from apps.pricingpage.models import *

# Helper function to get or create Bangla language
def get_or_create_bangla_language():
    try:
        bangla_language = Languages.objects.get(code="bn")
    except Languages.DoesNotExist:
        bangla_language = Languages.objects.create(name="Bangla", code="bn", is_rtl=False)
    return bangla_language

@receiver(post_migrate)
def create_bangla_pricing_entries(sender, **kwargs):
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

    # Get or create the Bangla language
    bangla_language = get_or_create_bangla_language()

    # Check if any records exist in the pricing table for Bangla
    if not pricing.objects.filter(language=bangla_language).exists():
        bangla_pricing_entries = [
            {
                "title": "প্রফেশনাল",
                "price": "৫০০০",
                "description": """
                    <ul>
                        <li>১০ পেজের রেসপনসিভ ওয়েবসাইট</li>
                        <li>৫ পিপিসি ক্যাম্পেইন</li>
                        <li>১০ এসইও কীওয়ার্ড</li>
                        <li>৫ ফেসবুক ক্যাম্পেইন</li>
                        <li>২ ভিডিও ক্যাম্পেইন</li>
                    </ul>
                """,
                "button_text": "যোগাযোগ করুন",
                "button_url": "/contact-us",
                "is_featured": False,
                "featured_badge_title": None,
                "language": bangla_language,
            },
            {
                "title": "স্ট্যান্ডার্ড",
                "price": "১০০০০",
                "description": """
                    <ul>
                        <li>৫০ পেজের রেসপনসিভ ওয়েবসাইট</li>
                        <li>১০ পিপিসি ক্যাম্পেইন</li>
                        <li>২০ এসইও কীওয়ার্ড</li>
                        <li>১০ ফেসবুক ক্যাম্পেইন</li>
                        <li>৪ ভিডিও ক্যাম্পেইন</li>
                    </ul>
                """,
                "button_text": "যোগাযোগ করুন",
                "button_url": "/contact-us",
                "is_featured": True,
                "featured_badge_title": "জনপ্রিয়",
                "language": bangla_language,
            },
            {
                "title": "আলটিমেট",
                "price": "১৫০০০",
                "description": """
                    <ul>
                        <li>৩০ পেজের রেসপনসিভ ওয়েবসাইট</li>
                        <li>১৫ পিপিসি ক্যাম্পেইন</li>
                        <li>৩০ এসইও কীওয়ার্ড</li>
                        <li>১৫ ফেসবুক ক্যাম্পেইন</li>
                        <li>৬ ভিডিও ক্যাম্পেইন</li>
                    </ul>
                """,
                "button_text": "যোগাযোগ করুন",
                "button_url": "/contact-us",
                "is_featured": False,
                "featured_badge_title": None,
                "language": bangla_language,
            }
        ]

        # Create pricing entries in Bangla
        for entry in bangla_pricing_entries:
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
            print(f"Bangla Pricing plan '{entry['title']}' created.")
    else:
        print("Bangla Pricing entries already exist. Skipping creation.")


@receiver(post_migrate)
def create_bangla_pricing_section_title(sender, **kwargs):
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

    # Get or create the Bangla language
    bangla_language = get_or_create_bangla_language()

    # Check if any record exists in pricingSectionTitle for Bangla
    if not pricingSectionTitle.objects.filter(language=bangla_language).exists():
        pricingSectionTitle.objects.create(
            title_small="আমাদের মূল্য",
            title_big="আপনার জন্য সেরা প্ল্যান নির্বাচন করুন",
            language=bangla_language
        )
        print("Bangla Pricing Section Title created.")
    else:
        print("Bangla Pricing Section Title already exists. Skipping creation.")


@receiver(post_migrate)
def create_bangla_pricing_page_seo(sender, **kwargs):
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

    # Get or create the Bangla language
    bangla_language = get_or_create_bangla_language()

    # Check if any record exists in pricingPageSEO for Bangla
    if not pricingPageSEO.objects.filter(language=bangla_language).exists():
        pricingPageSEO.objects.create(
            meta_title="মূল্য নির্ধারণ",
            meta_description="দ্য কোডগ্রামার",
            language=bangla_language
        )
        print("Bangla Pricing Page SEO created.")
    else:
        print("Bangla Pricing Page SEO already exists. Skipping creation.")
