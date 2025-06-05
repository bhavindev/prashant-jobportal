import os
import requests
from django.core.files import File
from django.conf import settings
from django.db import connection
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from apps.lang.models import Languages
from apps.blog.models import *

# Helper function to get or create Bangla language
def get_or_create_bangla_language():
    try:
        bangla_language = Languages.objects.get(code="bn")
    except Languages.DoesNotExist:
        bangla_language = Languages.objects.create(name="Bangla", code="bn", is_rtl=False)
    return bangla_language

@receiver(post_migrate)
def create_bangla_blogs_and_categories(sender, **kwargs):
    if sender.name != 'apps.blog':
        return

    # Check if the blogCategory and blogs tables exist
    category_table_name = blogCategory._meta.db_table
    blog_table_name = blogs._meta.db_table

    with connection.cursor() as cursor:
        cursor.execute(f"""
            SELECT EXISTS (
                SELECT 1 
                FROM information_schema.tables 
                WHERE table_name = '{category_table_name}'
            );
        """)
        category_table_exists = cursor.fetchone()[0]

        cursor.execute(f"""
            SELECT EXISTS (
                SELECT 1 
                FROM information_schema.tables 
                WHERE table_name = '{blog_table_name}'
            );
        """)
        blog_table_exists = cursor.fetchone()[0]

    if not category_table_exists or not blog_table_exists:
        print(f"Table {category_table_name} or {blog_table_name} does not exist. Skipping creation.")
        return

    # Get the Bangla language
    bangla_language = get_or_create_bangla_language()

    # Create blog categories if they don't exist
    categories_data = [
        {"title": "ব্যবসা", "language": bangla_language},
        {"title": "শিক্ষা", "language": bangla_language},
    ]

    categories = {}

    for category_data in categories_data:
        category, created = blogCategory.objects.get_or_create(
            title=category_data["title"],
            defaults={"language": category_data["language"]}
        )
        categories[category_data["title"]] = category
        if created:
            print(f"Bangla Category '{category_data['title']}' created.")
        else:
            print(f"Bangla Category '{category_data['title']}' already exists. Skipping creation.")

    # Check if any blogs exist
    if not blogs.objects.filter(language=bangla_language).exists():
        # Blog data
        blog_entries = [
            {
                "thumbnail_url": "https://crm.thecodegrammer.net/media/blogs/1.jpg",
                "title": "দ্য কোডগ্রামার: ডিজিটাল উদ্ভাবনের শক্তি",
                "category": categories["ব্যবসা"],  # Set the correct foreign key for category
                "description": """
                    <p><strong>ফেসবুক কমার্সের মাধ্যমে আপনার পৌঁছান সর্বাধিক করুন</strong><br />
                    ফেসবুক কমার্স একটি ব্যবসার ফেসবুক পেজের মাধ্যমে ই-কমার্স কার্যক্রম পরিচালনা করার প্রক্রিয়া।</p>

                    <p>দ্য কোডগ্রামার এ, আমরা বিশ্বাস করি যে ফেসবুক কমার্স একটি গুরুত্বপূর্ণ ই-কমার্স কৌশল।</p>

                    <p>ব্যবসার জন্য ফেসবুক কমার্সের চ্যালেঞ্জ রয়েছে।</p>

                    <p>তবে ফেসবুক কমার্স ক্রমবর্ধমান জনপ্রিয় হয়ে উঠছে।</p>

                    <p>দ্য কোডগ্রামার আপনাকে এই শক্তিশালী সরঞ্জামটির সর্বাধিক ব্যবহার করতে সহায়তা করতে প্রস্তুত।</p>

                    <p>উপসংহারে, ফেসবুক কমার্স একটি মূল্যবান কৌশল।</p>
                """,
                "author": "দ্য কোডগ্রামার",
                "language": bangla_language,
            },
            {
                "thumbnail_url": "https://crm.thecodegrammer.net/media/blogs/2.jpg",
                "title": "স্টার্টআপের মিথগুলি সম্পর্কে সব কিছু",
                "category": categories["শিক্ষা"],  # Set the correct foreign key for category
                "description": """
                    <p><strong>ফেসবুক কমার্সের মাধ্যমে আপনার পৌঁছান সর্বাধিক করুন</strong><br />
                    ফেসবুক কমার্স একটি ব্যবসার ফেসবুক পেজের মাধ্যমে ই-কমার্স কার্যক্রম পরিচালনা করার প্রক্রিয়া।</p>

                    <p>দ্য কোডগ্রামার এ, আমরা বিশ্বাস করি যে ফেসবুক কমার্স একটি গুরুত্বপূর্ণ ই-কমার্স কৌশল।</p>

                    <p>ব্যবসার জন্য ফেসবুক কমার্সের চ্যালেঞ্জ রয়েছে।</p>

                    <p>তবে ফেসবুক কমার্স ক্রমবর্ধমান জনপ্রিয় হয়ে উঠছে।</p>

                    <p>দ্য কোডগ্রামার আপনাকে এই শক্তিশালী সরঞ্জামটির সর্বাধিক ব্যবহার করতে সহায়তা করতে প্রস্তুত।</p>

                    <p>উপসংহারে, ফেসবুক কমার্স একটি মূল্যবান কৌশল।</p>
                """,
                "author": "দ্য কোডগ্রামার",
                "language": bangla_language,
            }
        ]

        # Process each blog entry
        for blog_data in blog_entries:
            thumbnail_url = blog_data["thumbnail_url"]
            image_name = os.path.basename(thumbnail_url)
            image_dir = os.path.join(settings.MEDIA_ROOT, 'blogs')
            image_path = os.path.join(image_dir, image_name)

            # Create the directory if it doesn't exist
            if not os.path.exists(image_dir):
                os.makedirs(image_dir)

            # Download the image if it doesn't exist locally
            if not os.path.exists(image_path):
                response = requests.get(thumbnail_url)
                if response.status_code == 200:
                    with open(image_path, 'wb') as f:
                        f.write(response.content)
                    print(f"Thumbnail {image_name} downloaded.")
                else:
                    print(f"Failed to download thumbnail from {thumbnail_url}")
                    continue

            # Create the blog entry
            with open(image_path, 'rb') as f:
                blog_record = blogs.objects.create(
                    title=blog_data["title"],
                    category=blog_data["category"],
                    description=blog_data["description"],
                    author=blog_data["author"],
                    language=blog_data["language"],
                )
                blog_record.thumbnail.save(image_name, File(f))
                print(f"Bangla Blog '{blog_data['title']}' created with thumbnail.")
    else:
        print("Bangla Blogs already exist. Skipping creation.")


@receiver(post_migrate)
def create_bangla_blog_page_seo(sender, **kwargs):
    if sender.name != 'apps.homepage':
        return

    # Check if the blogPageSEO table exists
    seo_table_name = blogPageSEO._meta.db_table

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
        print(f"Table {seo_table_name} does not exist. Skipping blogPageSEO creation.")
        return

    # Get the Bangla language
    bangla_language = get_or_create_bangla_language()

    # Check if any record exists in blogPageSEO
    if not blogPageSEO.objects.filter(language=bangla_language).exists():
        blogPageSEO.objects.create(
            meta_title="ব্লগ",
            meta_description="দ্য কোডগ্রামার",
            language=bangla_language
        )
        print("Bangla Blog Page SEO created.")
    else:
        print("Bangla Blog Page SEO already exists. Skipping creation.")
