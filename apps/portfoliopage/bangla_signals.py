from django.db import connection
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from apps.lang.models import Languages
from apps.portfoliopage.models import *

# Helper function to get or create Bangla language
def get_or_create_bangla_language():
    try:
        bangla_language = Languages.objects.get(code="bn")
    except Languages.DoesNotExist:
        bangla_language = Languages.objects.create(name="Bangla", code="bn", is_rtl=False)
    return bangla_language

@receiver(post_migrate)
def create_portfolio_page_seo(sender, **kwargs):
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

    # Get the default language
    try:
        default_language = Languages.objects.get(is_default=True)
    except Languages.DoesNotExist:
        default_language = Languages.objects.create(name="English", code="en", is_default=True)

    # Check if any record exists in PortfolioPageSEO for English
    if not PortfolioPageSEO.objects.filter(language=default_language).exists():
        PortfolioPageSEO.objects.create(
            meta_title="Projects",
            meta_description="The CodeGrammer",
            language=default_language
        )
        print("Portfolio Page SEO (English) created.")
    else:
        print("Portfolio Page SEO (English) already exists. Skipping creation.")


@receiver(post_migrate)
def create_bangla_portfolio_page_seo(sender, **kwargs):
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

    # Get or create the Bangla language
    bangla_language = get_or_create_bangla_language()

    # Check if any record exists in PortfolioPageSEO for Bangla
    if not PortfolioPageSEO.objects.filter(language=bangla_language).exists():
        PortfolioPageSEO.objects.create(
            meta_title="প্রকল্পসমূহ",
            meta_description="দ্য কোডগ্রামার",
            language=bangla_language
        )
        print("Portfolio Page SEO (Bangla) created.")
    else:
        print("Portfolio Page SEO (Bangla) already exists. Skipping creation.")