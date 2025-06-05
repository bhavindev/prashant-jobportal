from django.db import connection
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from apps.lang.models import Languages
from apps.contactpage.models import *

# Helper function to get or create Bangla language
def get_or_create_bangla_language():
    try:
        bangla_language = Languages.objects.get(code="bn")
    except Languages.DoesNotExist:
        bangla_language = Languages.objects.create(name="Bangla", code="bn", is_rtl=False)
    return bangla_language

@receiver(post_migrate)
def create_bangla_contact_info(sender, **kwargs):
    if sender.name != 'apps.contactpage':
        return

    # Check if the ContactInfo table exists
    contact_info_table_name = ContactInfo._meta.db_table

    with connection.cursor() as cursor:
        cursor.execute(f"""
            SELECT EXISTS (
                SELECT 1 
                FROM information_schema.tables 
                WHERE table_name = '{contact_info_table_name}'
            );
        """)
        contact_info_table_exists = cursor.fetchone()[0]

    if not contact_info_table_exists:
        print(f"Table {contact_info_table_name} does not exist. Skipping ContactInfo creation.")
        return

    # Get the Bangla language
    bangla_language = get_or_create_bangla_language()

    # Check if any record exists in ContactInfo for Bangla
    if not ContactInfo.objects.filter(language=bangla_language).exists():
        ContactInfo.objects.create(
            box1_icon="fas fa-phone-volume",
            box1_title="আজই কল করুন",
            box1_description='<p><a href="tel:+8801620673388">+880 1620 673388</a></p>',
            
            box2_icon="fas fa-envelope",
            box2_title="আমাদের ইমেল",
            box2_description='<p><a href="mailto:admin@thecodegrammer.net">admin@thecodegrammer.net</a></p>',
            
            box3_icon="fas fa-map",
            box3_title="আমাদের ঠিকানা",
            box3_description="<p>এনইউ, গাজীপুর-১৭০৪, ঢাকা</p>",
            iframe_title="আমাদের অবস্থান",
            map_iframe="""
                <iframe style="border: 0;" src="https://maps.google.com/maps?q=Google,%20Mountain%20View,%20California,%20United%20States&amp;t=k&amp;z=13&amp;ie=UTF8&amp;iwloc=&amp;output=embed" width="100%" height="450" allowfullscreen=""></iframe>
            """,
            
            form_title="আমাদের একটি বার্তা পাঠান",
            
            name_field_label="নাম",
            name_field_placeholder="আপনার নাম",
            
            email_field_label="ইমেল",
            email_field_placeholder="example@email.com",
            
            phone_field_label="ফোন",
            phone_field_placeholder="+88012345678",
            
            message_field_label="বার্তা",
            message_field_placeholder="আপনার প্রশ্ন লিখুন",
            
            upload_field_label="ফাইল আপলোড করুন",
            
            submit_button_text="জমা দিন",
            language=bangla_language
        )
        print("Bangla Contact Info created.")
    else:
        print("Bangla Contact Info already exists. Skipping creation.")

@receiver(post_migrate)
def create_bangla_contact_page_seo(sender, **kwargs):
    if sender.name != 'apps.contactpage':
        return

    # Check if the ContactPageSEO table exists
    contact_page_seo_table_name = ContactPageSEO._meta.db_table

    with connection.cursor() as cursor:
        cursor.execute(f"""
            SELECT EXISTS (
                SELECT 1 
                FROM information_schema.tables 
                WHERE table_name = '{contact_page_seo_table_name}'
            );
        """)
        contact_page_seo_table_exists = cursor.fetchone()[0]

    if not contact_page_seo_table_exists:
        print(f"Table {contact_page_seo_table_name} does not exist. Skipping ContactPageSEO creation.")
        return

    # Get the Bangla language
    bangla_language = get_or_create_bangla_language()

    # Check if any record exists in ContactPageSEO for Bangla
    if not ContactPageSEO.objects.filter(language=bangla_language).exists():
        ContactPageSEO.objects.create(
            meta_title="যোগাযোগ করুন",
            meta_description="দ্য কোডগ্রামার",
            language=bangla_language
        )
        print("Bangla Contact Page SEO created.")
    else:
        print("Bangla Contact Page SEO already exists. Skipping creation.")
