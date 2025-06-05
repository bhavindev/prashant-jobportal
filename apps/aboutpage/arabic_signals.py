import os
import requests
from django.core.files import File
from django.conf import settings
from django.db import connection
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from apps.lang.models import Languages
from apps.homepage.models import clientSectionTitle
from apps.aboutpage.models import *

@receiver(post_migrate)
def create_arabic_clients(sender, **kwargs):
    if sender.name != 'apps.homepage' and sender.name != 'apps.aboutpage':
        return

    # Check if the clientsSection and clientSectionTitle tables exist
    clients_table_name = clientsSection._meta.db_table
    clients_title_table_name = clientSectionTitle._meta.db_table

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT EXISTS (
                SELECT 1 
                FROM information_schema.tables 
                WHERE table_name = %s
            );
        """, [clients_table_name])
        clients_table_exists = cursor.fetchone()[0]

        cursor.execute("""
            SELECT EXISTS (
                SELECT 1 
                FROM information_schema.tables 
                WHERE table_name = %s
            );
        """, [clients_title_table_name])
        clients_title_table_exists = cursor.fetchone()[0]

    if not clients_table_exists or not clients_title_table_exists:
        print(f"Clients or clients title tables do not exist. Skipping creation.")
        return

    # Get the Arabic language
    try:
        arabic_language = Languages.objects.get(code="ar")
    except Languages.DoesNotExist:
        arabic_language = Languages.objects.create(name="Arabic", code="ar", is_rtl=True)

    # Check if any record exists in clientSectionTitle
    if not clientSectionTitle.objects.filter(language=arabic_language).exists():
        clientSectionTitle.objects.create(
            title_small="أهم العملاء",
            title_big="لقد قمنا ببناء حلول ل...",
            language=arabic_language
        )
        print("Arabic client section title created.")
    else:
        print("Arabic client section title already exists. Skipping creation.")

    # Check if any record exists in clientsSection
    if not clientsSection.objects.filter(language=arabic_language).exists():
        clients = [
            {
                "company_name": "عميل 01",
                "company_url": "#",
                "image_url": "https://crm.thecodegrammer.net/media/clients/brand-1.png",
            },
            {
                "company_name": "عميل 02",
                "company_url": "#",
                "image_url": "https://crm.thecodegrammer.net/media/clients/brand-2.png",
            },
            {
                "company_name": "عميل 03",
                "company_url": "#",
                "image_url": "https://crm.thecodegrammer.net/media/clients/brand-3.png",
            },
            {
                "company_name": "عميل 04",
                "company_url": "#",
                "image_url": "https://crm.thecodegrammer.net/media/clients/brand-4.png",
            }
        ]

        # Create clientsSection entries
        for client in clients:
            image_url = client["image_url"]
            image_name = os.path.basename(image_url)
            image_dir = os.path.join(settings.MEDIA_ROOT, 'clients')
            image_path = os.path.join(image_dir, image_name)

            if not os.path.exists(image_dir):
                os.makedirs(image_dir)

            if not os.path.exists(image_path):
                response = requests.get(image_url)
                if response.status_code == 200:
                    with open(image_path, 'wb') as f:
                        f.write(response.content)
                    print(f"Image {image_name} downloaded.")
                else:
                    print(f"Failed to download image from {image_url}")
                    continue

            with open(image_path, 'rb') as f:
                client_record = clientsSection.objects.create(
                    company_name=client["company_name"],
                    company_url=client["company_url"],
                    language=arabic_language
                )
                client_record.image.save(image_name, File(f))
                print(f"Client '{client['company_name']}' created with image.")
    else:
        print("Arabic clients already exist. Skipping creation.")


@receiver(post_migrate)
def create_arabic_about_settings(sender, **kwargs):
    if sender.name != 'apps.aboutpage':
        return

    about_table_name = aboutSettings._meta.db_table

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT EXISTS (
                SELECT 1 
                FROM information_schema.tables 
                WHERE table_name = %s
            );
        """, [about_table_name])
        about_table_exists = cursor.fetchone()[0]

    if not about_table_exists:
        print(f"Table {about_table_name} does not exist. Skipping aboutSettings creation.")
        return

    # Get the Arabic language
    try:
        arabic_language = Languages.objects.get(code="ar")
    except Languages.DoesNotExist:
        arabic_language = Languages.objects.create(name="Arabic", code="ar", is_rtl=True)

    # Check if any record exists in aboutSettings
    if not aboutSettings.objects.filter(language=arabic_language).exists():
        aboutSettings.objects.create(
            title_white="مرحبًا بك في",
            title_red="The CodeGrammer.",
            heading="بناء البرمجيات من أجل مغيري العالم",
            description="""
                <p>مرحبًا بك في The CodeGrammer، شركة تطوير ويب وتطبيقات رائدة مكرسة لإنشاء حلول رقمية مخصصة تساعد الشركات على الازدهار في العالم الرقمي السريع. مع التركيز القوي على الابتكار والإبداع والتميز الفني، نتخصص في تقديم تطبيقات الويب وحلول الهاتف المحمول المخصصة التي تلبي احتياجات عملائنا الفريدة.</p>
            """,
            count_title1="سنوات في السوق",
            years_of_experience=3,
            count_title2="المشاريع التي تم تسليمها حتى الآن",
            project_delivered=250,
            button_text="تواصل معنا",
            button_url="/contact-us",
            language=arabic_language
        )
        print("Arabic about settings created.")
    else:
        print("Arabic about settings already exist. Skipping creation.")


@receiver(post_migrate)
def create_arabic_team_members_and_title(sender, **kwargs):
    if sender.name != 'apps.aboutpage':
        return

    team_table_name = teamSection._meta.db_table
    team_title_table_name = teamSectionTitle._meta.db_table

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT EXISTS (
                SELECT 1 
                FROM information_schema.tables 
                WHERE table_name = %s
            );
        """, [team_table_name])
        team_table_exists = cursor.fetchone()[0]

        cursor.execute("""
            SELECT EXISTS (
                SELECT 1 
                FROM information_schema.tables 
                WHERE table_name = %s
            );
        """, [team_title_table_name])
        team_title_table_exists = cursor.fetchone()[0]

    if not team_table_exists or not team_title_table_exists:
        print(f"Team or team title tables do not exist. Skipping creation.")
        return

    # Get the Arabic language
    try:
        arabic_language = Languages.objects.get(code="ar")
    except Languages.DoesNotExist:
        arabic_language = Languages.objects.create(name="Arabic", code="ar", is_rtl=True)

    if not teamSectionTitle.objects.filter(language=arabic_language).exists():
        teamSectionTitle.objects.create(
            title_small="قيمنا",
            title_big="قابل الفريق",
            language=arabic_language
        )
        print("Arabic team section title created.")
    else:
        print("Arabic team section title already exists. Skipping creation.")

    if not teamSection.objects.filter(language=arabic_language).exists():
        team_members = [
            {
                "name": "أندرو رايكو",
                "about": "The CodeGrammer، بقيادة أندرو رايكو، هو مجتمع مزدهر لعشاق البرمجة.",
                "position": "المؤسس والمدير",
                "image_url": "https://crm.thecodegrammer.net/media/team/team-1.jpg",
            },
            {
                "name": "أليكس مايرو",
                "about": "أليكس مايرو هو أحد عشاق [Interest] من [Hometown].",
                "position": "المدير",
                "image_url": "https://crm.thecodegrammer.net/media/team/team-3.jpg",
            },
            {
                "name": "ثورن أوكنديلد",
                "about": "ثورن أوكنديلد هو أحد عشاق [Interest] من [Hometown].",
                "position": "المطور",
                "image_url": "https://crm.thecodegrammer.net/media/team/team-1.jpg",
            },
            {
                "name": "أدريان أودري",
                "about": "أدريان أودري هو أحد عشاق [Interest] من [Hometown].",
                "position": "المصمم",
                "image_url": "https://crm.thecodegrammer.net/media/team/team-3.jpg",
            }
        ]

        for member in team_members:
            image_url = member["image_url"]
            image_name = os.path.basename(image_url)
            image_dir = os.path.join(settings.MEDIA_ROOT, 'team')
            image_path = os.path.join(image_dir, image_name)

            if not os.path.exists(image_dir):
                os.makedirs(image_dir)

            if not os.path.exists(image_path):
                response = requests.get(image_url)
                if response.status_code == 200:
                    with open(image_path, 'wb') as f:
                        f.write(response.content)
                    print(f"Image {image_name} downloaded.")
                else:
                    print(f"Failed to download image from {image_url}")
                    continue

            with open(image_path, 'rb') as f:
                team_record = teamSection.objects.create(
                    name=member["name"],
                    about=member["about"],
                    position=member["position"],
                    language=arabic_language
                )
                team_record.image.save(image_name, File(f))
                print(f"Team member '{member['name']}' created with image.")
    else:
        print("Arabic team members already exist. Skipping creation.")


@receiver(post_migrate)
def create_arabic_about_page_seo(sender, **kwargs):
    if sender.name != 'apps.aboutpage':
        return

    seo_table_name = AboutPageSEO._meta.db_table

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT EXISTS (
                SELECT 1 
                FROM information_schema.tables 
                WHERE table_name = %s
            );
        """, [seo_table_name])
        seo_table_exists = cursor.fetchone()[0]

    if not seo_table_exists:
        print(f"Table {seo_table_name} does not exist. Skipping AboutPageSEO creation.")
        return

    # Get the Arabic language
    try:
        arabic_language = Languages.objects.get(code="ar")
    except Languages.DoesNotExist:
        arabic_language = Languages.objects.create(name="Arabic", code="ar", is_rtl=True)

    if not AboutPageSEO.objects.filter(language=arabic_language).exists():
        AboutPageSEO.objects.create(
            meta_title="من نحن",
            meta_description="The CodeGrammer",
            language=arabic_language
        )
        print("Arabic About Page SEO created.")
    else:
        print("Arabic About Page SEO already exists. Skipping creation.")
