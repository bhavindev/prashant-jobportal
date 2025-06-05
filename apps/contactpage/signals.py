from django.db import connection
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from apps.lang.models import Languages
from apps.contactpage.models import *

@receiver(post_migrate)
def create_contact_info(sender, **kwargs):
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

    # Get the default language
    try:
        default_language = Languages.objects.get(is_default=True)
    except Languages.DoesNotExist:
        default_language = Languages.objects.create(name="English", code="en", is_default=True)

    # Check if any record exists in ContactInfo
    if not ContactInfo.objects.exists():
        ContactInfo.objects.create(
            box1_icon="fas fa-phone-volume",
            box1_title="Call us today",
            box1_description='<p><a href="tel:+8801620673388">+880 1620 673388</a></p>',
            
            box2_icon="fas fa-envelope",
            box2_title="Our emails",
            box2_description='<p><a href="mailto:admin@thecodegrammer.net">admin@thecodegrammer.net</a></p>',
            
            box3_icon="fas fa-map",
            box3_title="Our address",
            box3_description="<p>NU, Gazipur-1704, Dhaka</p>",
            iframe_title="Where we are",
            map_iframe="""
                <iframe style="border: 0;" src="https://maps.google.com/maps?q=Google,%20Mountain%20View,%20California,%20United%20States&amp;t=k&amp;z=13&amp;ie=UTF8&amp;iwloc=&amp;output=embed" width="100%" height="450" allowfullscreen=""></iframe>
            """,
            
            form_title="Send us a message",
            
            name_field_label="Name",
            name_field_placeholder="Jhon Doe",
            
            email_field_label="Email",
            email_field_placeholder="example@email.com",
            
            phone_field_label="Phone",
            phone_field_placeholder="+12345678",
            
            message_field_label="Message",
            message_field_placeholder="Explain your query",
            
            upload_field_label="Upload File",
            
            submit_button_text="Submit",
            language=default_language
        )
        print("Contact Info created.")
    else:
        print("Contact Info already exists. Skipping creation.")


@receiver(post_migrate)
def create_contact_page_seo(sender, **kwargs):
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

    # Get the default language
    try:
        default_language = Languages.objects.get(is_default=True)
    except Languages.DoesNotExist:
        print("Default language not found.")
        return

    # Check if any record exists in ContactPageSEO
    if not ContactPageSEO.objects.exists():
        ContactPageSEO.objects.create(
            meta_title="Contact Us",
            meta_description="The CodeGrammer",
            language=default_language
        )
        print("Contact Page SEO created.")
    else:
        print("Contact Page SEO already exists. Skipping creation.")