from django.db import connection
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from apps.lang.models import Languages
from apps.portfoliopage.models import *

@receiver(post_migrate)
def create_arabic_portfolio_page_seo(sender, **kwargs):
    if sender.name != 'apps.portfoliopage':
        return

    # Check if the PortfolioPageSEO table exists
    seo_table_name = PortfolioPageSEO._meta.db_table

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
        print(f"Table {seo_table_name} does not exist. Skipping PortfolioPageSEO creation.")
        return

    # Get the Arabic language
    try:
        arabic_language = Languages.objects.get(code="ar")
    except Languages.DoesNotExist:
        arabic_language = Languages.objects.create(name="Arabic", code="ar", is_rtl=True)

    # Check if any record exists in PortfolioPageSEO for Arabic
    if not PortfolioPageSEO.objects.filter(language=arabic_language).exists():
        PortfolioPageSEO.objects.create(
            meta_title="المشاريع",
            meta_description="The CodeGrammer",
            language=arabic_language
        )
        print("Arabic Portfolio Page SEO created.")
    else:
        print("Arabic Portfolio Page SEO already exists. Skipping creation.")
