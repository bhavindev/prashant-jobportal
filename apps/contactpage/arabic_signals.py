from django.db import connection
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from apps.lang.models import Languages
from apps.contactpage.models import *

@receiver(post_migrate)
def create_arabic_contact_info(sender, **kwargs):
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

    # Get the Arabic language
    try:
        arabic_language = Languages.objects.get(code="ar")
    except Languages.DoesNotExist:
        arabic_language = Languages.objects.create(name="Arabic", code="ar", is_rtl=True)

    # Check if any record exists in ContactInfo for Arabic
    if not ContactInfo.objects.filter(language=arabic_language).exists():
        ContactInfo.objects.create(
            box1_icon="fas fa-phone-volume",
            box1_title="اتصل بنا اليوم",
            box1_description='<p><a href="tel:+8801620673388">+880 1620 673388</a></p>',
            
            box2_icon="fas fa-envelope",
            box2_title="بريدنا الإلكتروني",
            box2_description='<p><a href="mailto:admin@thecodegrammer.net">admin@thecodegrammer.net</a></p>',
            
            box3_icon="fas fa-map",
            box3_title="عنواننا",
            box3_description="<p>NU، غازيبور-1704، دكا</p>",
            
            iframe_title="أين نحن",
            map_iframe="""
                <iframe style="border: 0;" src="https://maps.google.com/maps?q=Google,%20Mountain%20View,%20California,%20United%20States&amp;t=k&amp;z=13&amp;ie=UTF8&amp;iwloc=&amp;output=embed" width="100%" height="450" allowfullscreen=""></iframe>
            """,
            
            form_title="أرسل لنا رسالة",
            
            name_field_label="الاسم",
            name_field_placeholder="محمد أحمد",
            
            email_field_label="البريد الإلكتروني",
            email_field_placeholder="example@email.com",
            
            phone_field_label="الهاتف",
            phone_field_placeholder="+12345678",
            
            message_field_label="رسالة",
            message_field_placeholder="اشرح استفسارك",
            
            upload_field_label="تحميل الملف",
            
            submit_button_text="إرسال",
            language=arabic_language
        )
        print("Arabic Contact Info created.")
    else:
        print("Arabic Contact Info already exists. Skipping creation.")


@receiver(post_migrate)
def create_arabic_contact_page_seo(sender, **kwargs):
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

    # Get the Arabic language
    try:
        arabic_language = Languages.objects.get(code="ar")
    except Languages.DoesNotExist:
        arabic_language = Languages.objects.create(name="Arabic", code="ar", is_rtl=True)

    # Check if any record exists in ContactPageSEO for Arabic
    if not ContactPageSEO.objects.filter(language=arabic_language).exists():
        ContactPageSEO.objects.create(
            meta_title="اتصل بنا",
            meta_description="The CodeGrammer",
            language=arabic_language
        )
        print("Arabic Contact Page SEO created.")
    else:
        print("Arabic Contact Page SEO already exists. Skipping creation.")
