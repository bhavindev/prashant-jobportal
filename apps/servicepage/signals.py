from django.db import connection
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from apps.lang.models import Languages
from apps.servicepage.models import *

@receiver(post_migrate)
def create_service_page_seo(sender, **kwargs):
    if sender.name != 'apps.servicepage':
        return

    # Check if the ServicePageSEO table exists
    seo_table_name = ServicePageSEO._meta.db_table

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
        print(f"Table {seo_table_name} does not exist. Skipping ServicePageSEO creation.")
        return

    # Get the default language
    try:
        default_language = Languages.objects.get(is_default=True)
    except Languages.DoesNotExist:
        default_language = Languages.objects.create(name="English", code="en", is_default=True)

    # Check if any record exists in ServicePageSEO
    if not ServicePageSEO.objects.exists():
        ServicePageSEO.objects.create(
            meta_title="Services",
            meta_description="The CodeGrammer",
            language=default_language
        )
        print("Service Page SEO created.")
    else:
        print("Service Page SEO already exists. Skipping creation.")
