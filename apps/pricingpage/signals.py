from django.db import connection
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from apps.lang.models import Languages
from apps.pricingpage.models import *

@receiver(post_migrate)
def create_pricing_entries(sender, **kwargs):
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

    # Get the default language
    try:
        default_language = Languages.objects.get(is_default=True)
    except Languages.DoesNotExist:
        default_language = Languages.objects.create(name="English", code="en", is_default=True)

    # Check if any records exist in the pricing table
    if not pricing.objects.exists():
        pricing_entries = [
            {
                "title": "Professional",
                "price": "5000",
                "description": """
                    <ul>
                        <li>10 Pages Responsive Website</li>
                        <li>5 PPC Campaigns</li>
                        <li>10 SEO Keywords</li>
                        <li>5 Facebook Camplaigns</li>
                        <li>2 Video Camplaigns</li>
                    </ul>
                """,
                "button_text": "Contact Us",
                "button_url": "/contact-us",
                "is_featured": False,
                "featured_badge_title": None,
                "language": default_language,
            },
            {
                "title": "Standard",
                "price": "10000",
                "description": """
                    <ul>
                        <li>50 Pages Responsive Website</li>
                        <li>10 PPC Campaigns</li>
                        <li>20 SEO Keywords</li>
                        <li>10 Facebook Camplaigns</li>
                        <li>4 Video Camplaigns</li>
                    </ul>
                """,
                "button_text": "Contact Us",
                "button_url": "/contact-us",
                "is_featured": True,
                "featured_badge_title": "Popular",
                "language": default_language,
            },
            {
                "title": "Ultimate",
                "price": "15000",
                "description": """
                    <ul>
                        <li>30 Pages Responsive Website</li>
                        <li>15 PPC Campaigns</li>
                        <li>30 SEO Keywords</li>
                        <li>15 Facebook Camplaigns</li>
                        <li>6 Video Camplaigns</li>
                    </ul>
                """,
                "button_text": "Contact Us",
                "button_url": "/contact-us",
                "is_featured": False,
                "featured_badge_title": None,
                "language": default_language,
            }
        ]

        # Create pricing entries
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
            print(f"Pricing plan '{entry['title']}' created.")
    else:
        print("Pricing entries already exist. Skipping creation.")


@receiver(post_migrate)
def create_pricing_section_title(sender, **kwargs):
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

    # Get the default language
    try:
        default_language = Languages.objects.get(is_default=True)
    except Languages.DoesNotExist:
        default_language = Languages.objects.create(name="English", code="en", is_default=True)

    # Check if any record exists in pricingSectionTitle
    if not pricingSectionTitle.objects.exists():
        pricingSectionTitle.objects.create(
            title_small="Our Pricing",
            title_big="Choose the Best Plan for You",
            language=default_language
        )
        print("Pricing Section Title created.")
    else:
        print("Pricing Section Title already exists. Skipping creation.")


@receiver(post_migrate)
def create_pricing_page_seo(sender, **kwargs):
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

    # Get the default language
    try:
        default_language = Languages.objects.get(is_default=True)
    except Languages.DoesNotExist:
        default_language = Languages.objects.create(name="English", code="en", is_default=True)

    # Check if any record exists in pricingPageSEO
    if not pricingPageSEO.objects.exists():
        pricingPageSEO.objects.create(
            meta_title="Pricing",
            meta_description="The CodeGrammer",
            language=default_language
        )
        print("Pricing Page SEO created.")
    else:
        print("Pricing Page SEO already exists. Skipping creation.")
        
        