from django.db import connection
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from apps.lang.models import Languages
from apps.servicepage.models import *

@receiver(post_migrate)
def create_arabic_service_page_seo(sender, **kwargs):
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

    # Get the Arabic language
    try:
        arabic_language = Languages.objects.get(code="ar")
    except Languages.DoesNotExist:
        arabic_language = Languages.objects.create(name="Arabic", code="ar", is_rtl=True)

    # Check if any record exists in ServicePageSEO for Arabic
    if not ServicePageSEO.objects.filter(language=arabic_language).exists():
        ServicePageSEO.objects.create(
            meta_title="الخدمات",
            meta_description="The CodeGrammer",
            language=arabic_language
        )
        print("Arabic Service Page SEO created.")
    else:
        print("Arabic Service Page SEO already exists. Skipping creation.")
