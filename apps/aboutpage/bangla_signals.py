import os
import requests
from django.core.files import File
from django.conf import settings
from django.db import connection
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from apps.lang.models import Languages
from apps.homepage.models import clientSectionTitle
from apps.aboutpage.models import aboutSettings, teamSection, teamSectionTitle, AboutPageSEO, clientsSection

# Function to create Bangla language
def get_or_create_bangla_language():
    try:
        bangla_language = Languages.objects.get(code="bn")
    except Languages.DoesNotExist:
        bangla_language = Languages.objects.create(name="Bangla", code="bn", is_rtl=False)
    return bangla_language

@receiver(post_migrate)
def create_bangla_clients(sender, **kwargs):
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

    # Get the Bangla language
    bangla_language = get_or_create_bangla_language()

    # Check if any record exists in clientSectionTitle
    if not clientSectionTitle.objects.filter(language=bangla_language).exists():
        clientSectionTitle.objects.create(
            title_small="শীর্ষ ক্লায়েন্ট",
            title_big="আমরা যাদের জন্য সমাধান তৈরি করেছি",
            language=bangla_language
        )
        print("Bangla client section title created.")
    else:
        print("Bangla client section title already exists. Skipping creation.")

    # Check if any record exists in clientsSection
    if not clientsSection.objects.filter(language=bangla_language).exists():
        clients = [
            {
                "company_name": "ক্লায়েন্ট ০১",
                "company_url": "#",
                "image_url": "https://crm.thecodegrammer.net/media/clients/brand-1.png",
            },
            {
                "company_name": "ক্লায়েন্ট ০২",
                "company_url": "#",
                "image_url": "https://crm.thecodegrammer.net/media/clients/brand-2.png",
            },
            {
                "company_name": "ক্লায়েন্ট ০৩",
                "company_url": "#",
                "image_url": "https://crm.thecodegrammer.net/media/clients/brand-3.png",
            },
            {
                "company_name": "ক্লায়েন্ট ০৪",
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

            # Create the directory if it doesn't exist
            if not os.path.exists(image_dir):
                os.makedirs(image_dir)

            # Download the image if it doesn't exist locally
            if not os.path.exists(image_path):
                response = requests.get(image_url)
                if response.status_code == 200:
                    with open(image_path, 'wb') as f:
                        f.write(response.content)
                    print(f"Image {image_name} downloaded.")
                else:
                    print(f"Failed to download image from {image_url}")
                    continue

            # Create the client entry
            with open(image_path, 'rb') as f:
                client_record = clientsSection.objects.create(
                    company_name=client["company_name"],
                    company_url=client["company_url"],
                    language=bangla_language
                )
                client_record.image.save(image_name, File(f))
                print(f"Bangla Client '{client['company_name']}' created with image.")
    else:
        print("Bangla Clients already exist. Skipping creation.")


@receiver(post_migrate)
def create_bangla_about_settings(sender, **kwargs):
    if sender.name != 'apps.aboutpage':
        return

    # Check if the aboutSettings table exists
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

    # Get the Bangla language
    bangla_language = get_or_create_bangla_language()

    # Check if any record exists in aboutSettings
    if not aboutSettings.objects.filter(language=bangla_language).exists():
        # Create the aboutSettings entry
        about_record = aboutSettings.objects.create(
            title_white="স্বাগতম",
            title_red="দ্য কোডগ্রামার এ",
            heading="বিশ্ব পরিবর্তনকারীদের জন্য সফটওয়্যার তৈরি করা",
            description="""
                <p>স্বাগতম দ্য কোডগ্রামার, একটি শীর্ষস্থানীয় ওয়েব এবং অ্যাপ্লিকেশন ডেভেলপমেন্ট কোম্পানি, যা ব্যবসার উন্নতির জন্য ডিজিটাল সমাধান তৈরি করে।</p>
                <h3>আমরা কারা</h3>
                <p>কোডগ্রামারে, আমরা উদ্ভাবনের প্রতি অনুরাগী এবং ডিজিটাল পরিবর্তনের জন্য দৃঢ়প্রতিজ্ঞ।</p>
                <h3>আমাদের সেবা</h3>
                <ul>
                    <li><p><strong>কাস্টম ওয়েব অ্যাপ্লিকেশন:</strong> উচ্চ কার্যক্ষম ওয়েব অ্যাপ্লিকেশন ডিজাইন ও ডেভেলপ করি।</p></li>
                    <li><p><strong>মোবাইল অ্যাপ ডেভেলপমেন্ট:</strong> কাস্টম মোবাইল অ্যাপ যা আপনার ব্যবসার জন্য তৈরি।</p></li>
                    <li><p><strong>ইউআই/ইউএক্স ডিজাইন:</strong> ব্যবহারকারী অভিজ্ঞতার জন্য সুন্দর ও কার্যকর ডিজাইন।</p></li>
                </ul>
                <p><strong>যোগাযোগ করুন</strong> আজই এবং আপনার ডিজিটাল ভবিষ্যত গড়ুন আমাদের সঙ্গে।</p>
            """,
            count_title1="বছর",
            years_of_experience=3,
            count_title2="প্রকল্প সরবরাহ করা হয়েছে",
            project_delivered=250,
            button_text="যোগাযোগ করুন",
            button_url="/contact-us",
            language=bangla_language
        )
        print("Bangla About settings created.")
    else:
        print("Bangla About settings already exist. Skipping creation.")


@receiver(post_migrate)
def create_bangla_team_members_and_title(sender, **kwargs):
    if sender.name != 'apps.aboutpage':
        return

    # Check if the teamSection and teamSectionTitle tables exist
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

    # Get the Bangla language
    bangla_language = get_or_create_bangla_language()

    # Create teamSectionTitle if no record exists
    if not teamSectionTitle.objects.filter(language=bangla_language).exists():
        teamSectionTitle.objects.create(
            title_small="আমাদের মূল্যবোধ",
            title_big="পরিচিত হন আমাদের টিমের সঙ্গে",
            language=bangla_language
        )
        print("Bangla Team section title created.")
    else:
        print("Bangla Team section title already exists. Skipping creation.")

    # Check if any record exists in teamSection
    if not teamSection.objects.filter(language=bangla_language).exists():
        team_members = [
            {
                "name": "এন্ড্রু রাইকো",
                "about": "এন্ড্রু রাইকোর নেতৃত্বে কোডগ্রামার কোডিং প্রেমীদের একটি সম্প্রদায়।",
                "position": "প্রতিষ্ঠাতা ও পরিচালক",
                "image_url": "https://crm.thecodegrammer.net/media/team/team-1.jpg",
            },
            {
                "name": "অ্যালেক্স মাইরো",
                "about": "অ্যালেক্স মাইরো একজন উদ্ভাবনী ব্যক্তি যিনি প্রযুক্তির প্রতি অনুরাগী।",
                "position": "ম্যানেজার",
                "image_url": "https://crm.thecodegrammer.net/media/team/team-3.jpg",
            },
            {
                "name": "থোরেন ওকেনডিল্ড",
                "about": "থোরেন ওকেনডিল্ড কোডিং প্রেমী এবং উদ্ভাবনী প্রযুক্তির একনিষ্ঠ সেবক।",
                "position": "ডেভেলপার",
                "image_url": "https://crm.thecodegrammer.net/media/team/team-1.jpg",
            },
            {
                "name": "এড্রিয়ান ইওডরি",
                "about": "এড্রিয়ান ইওডরি, একজন ডিজাইনার এবং প্রযুক্তি অনুরাগী।",
                "position": "ডিজাইনার",
                "image_url": "https://crm.thecodegrammer.net/media/team/team-3.jpg",
            }
        ]

        # Create teamSection entries
        for member in team_members:
            image_url = member["image_url"]
            image_name = os.path.basename(image_url)
            image_dir = os.path.join(settings.MEDIA_ROOT, 'team')
            image_path = os.path.join(image_dir, image_name)

            # Create the directory if it doesn't exist
            if not os.path.exists(image_dir):
                os.makedirs(image_dir)

            # Download the image if it doesn't exist locally
            if not os.path.exists(image_path):
                response = requests.get(image_url)
                if response.status_code == 200:
                    with open(image_path, 'wb') as f:
                        f.write(response.content)
                    print(f"Image {image_name} downloaded.")
                else:
                    print(f"Failed to download image from {image_url}")
                    continue

            # Create the team member entry
            with open(image_path, 'rb') as f:
                team_record = teamSection.objects.create(
                    name=member["name"],
                    about=member["about"],
                    position=member["position"],
                    language=bangla_language
                )
                team_record.image.save(image_name, File(f))
                print(f"Bangla Team member '{member['name']}' created with image.")
    else:
        print("Bangla Team members already exist. Skipping creation.")


@receiver(post_migrate)
def create_bangla_about_page_seo(sender, **kwargs):
    if sender.name != 'apps.aboutpage':
        return

    # Check if the AboutPageSEO table exists
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

    # Get the Bangla language
    bangla_language = get_or_create_bangla_language()

    # Check if any record exists in AboutPageSEO
    if not AboutPageSEO.objects.filter(language=bangla_language).exists():
        AboutPageSEO.objects.create(
            meta_title="আমাদের সম্পর্কে",
            meta_description="দ্য কোডগ্রামার",
            language=bangla_language
        )
        print("Bangla About Page SEO created.")
    else:
        print("Bangla About Page SEO already exists. Skipping creation.")
