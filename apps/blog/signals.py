import os
import requests
from django.core.files import File
from django.conf import settings
from django.db import connection
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from apps.lang.models import Languages
from apps.blog.models import *

@receiver(post_migrate)
def create_blogs_and_categories(sender, **kwargs):
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

    # Get the default language
    try:
        default_language = Languages.objects.get(is_default=True)
    except Languages.DoesNotExist:
        default_language = Languages.objects.create(name="English", code="en", is_default=True)

    # Create blog categories if they don't exist
    categories_data = [
        {"title": "Business", "language": default_language},
        {"title": "Education", "language": default_language},
    ]

    categories = {}

    for category_data in categories_data:
        category, created = blogCategory.objects.get_or_create(
            title=category_data["title"],
            defaults={"language": category_data["language"]}
        )
        categories[category_data["title"]] = category
        if created:
            print(f"Category '{category_data['title']}' created.")
        else:
            print(f"Category '{category_data['title']}' already exists. Skipping creation.")

    # Check if any blogs exist
    if not blogs.objects.exists():
        # Blog data
        blog_entries = [
            {
                "thumbnail_url": "https://crm.thecodegrammer.net/media/blogs/1.jpg",
                "title": "The CodeGrammer : Power of Digital Innovation",
                "category": categories["Business"],  # Set the correct foreign key for category
                "description": """
                    <p><strong>Maximizing Your Reach With Facebook Commerce</strong><br />
                    F-commerce, or Facebook commerce, is the practice of conducting e-commerce activities through a business's Facebook page. This includes buying and selling products and services directly on the social media platform. With over 2.8 billion monthly active users, Facebook has become a powerful tool for businesses to reach and engage with their target audience.</p>

                    <p>At The CodeGrammer, we believe that f-commerce is a crucial component of any successful e-commerce strategy. One of the main advantages of f-commerce is the ability to reach a large and diverse audience. With over 2.8 billion monthly active users, Facebook allows businesses to target specific demographics, such as age, gender, and location, making it easier to reach potential customers. Additionally, businesses can use Facebook's built-in analytics to track engagement and conversions, providing valuable insights into the performance of their f-commerce efforts.</p>

                    <p>Another advantage of f-commerce is the ability to create a more personal and interactive shopping experience for customers. At The CodeGrammer, we utilize Facebook's features, such as comments and reviews, to engage with our customers and provide a more personalized shopping experience. This can help to build trust and loyalty with customers, leading to increased sales and repeat business.</p>

                    <p>However, there are also some challenges to f-commerce. One of the main challenges is the limited functionality of Facebook's e-commerce features. Businesses are currently limited in the types of products and services they can sell through Facebook and the payment options available. Additionally, businesses may struggle to stand out among the vast number of pages and products on the platform.</p>

                    <p>Despite these challenges, f-commerce is becoming an increasingly popular e-commerce strategy for businesses. As Facebook continues to improve its e-commerce features, it is likely that more businesses will begin to utilize the platform as a way to reach and engage with customers.</p>

                    <p>At The CodeGrammer, we understand the importance of f-commerce and have the expertise to help businesses make the most of this powerful tool. We can help businesses of all sizes increase their reach and drive sales through f-commerce by creating a personalized shopping experience, utilizing Facebook's analytics, and developing strategies to stand out on the platform.</p>

                    <p>In conclusion, f-commerce is a valuable strategy for businesses to reach and engage with customers. With the help of experts like The CodeGrammer, businesses can take full advantage of the opportunities presented by f-commerce and drive growth and success.</p>
                """,
                "author": "The CodeGrammer",
                "language": default_language,
            },
            {
                "thumbnail_url": "https://crm.thecodegrammer.net/media/blogs/2.jpg",
                "title": "All About The Myths Of Startup In Business",
                "category": categories["Education"],  # Set the correct foreign key for category
                "description": """
                    <p><strong>Maximizing Your Reach With Facebook Commerce</strong><br />
                    F-commerce, or Facebook commerce, is the practice of conducting e-commerce activities through a business's Facebook page. This includes buying and selling products and services directly on the social media platform. With over 2.8 billion monthly active users, Facebook has become a powerful tool for businesses to reach and engage with their target audience.</p>

                    <p>At The CodeGrammer, we believe that f-commerce is a crucial component of any successful e-commerce strategy. One of the main advantages of f-commerce is the ability to reach a large and diverse audience. With over 2.8 billion monthly active users, Facebook allows businesses to target specific demographics, such as age, gender, and location, making it easier to reach potential customers. Additionally, businesses can use Facebook's built-in analytics to track engagement and conversions, providing valuable insights into the performance of their f-commerce efforts.</p>

                    <p>Another advantage of f-commerce is the ability to create a more personal and interactive shopping experience for customers. At The CodeGrammer, we utilize Facebook's features, such as comments and reviews, to engage with our customers and provide a more personalized shopping experience. This can help to build trust and loyalty with customers, leading to increased sales and repeat business.</p>

                    <p>However, there are also some challenges to f-commerce. One of the main challenges is the limited functionality of Facebook's e-commerce features. Businesses are currently limited in the types of products and services they can sell through Facebook and the payment options available. Additionally, businesses may struggle to stand out among the vast number of pages and products on the platform.</p>

                    <p>Despite these challenges, f-commerce is becoming an increasingly popular e-commerce strategy for businesses. As Facebook continues to improve its e-commerce features, it is likely that more businesses will begin to utilize the platform as a way to reach and engage with customers.</p>

                    <p>At The CodeGrammer, we understand the importance of f-commerce and have the expertise to help businesses make the most of this powerful tool. We can help businesses of all sizes increase their reach and drive sales through f-commerce by creating a personalized shopping experience, utilizing Facebook's analytics, and developing strategies to stand out on the platform.</p>

                    <p>In conclusion, f-commerce is a valuable strategy for businesses to reach and engage with customers. With the help of experts like The CodeGrammer, businesses can take full advantage of the opportunities presented by f-commerce and drive growth and success.</p>
                """,
                "author": "The CodeGrammer",
                "language": default_language,
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
                print(f"Blog '{blog_data['title']}' created with thumbnail.")
    else:
        print("Blogs already exist. Skipping creation.")


@receiver(post_migrate)
def create_blog_page_seo(sender, **kwargs):
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

    # Get the default language
    try:
        default_language = Languages.objects.get(is_default=True)
    except Languages.DoesNotExist:
        default_language = Languages.objects.create(name="English", code="en", is_default=True)

    # Check if any record exists in blogPageSEO
    if not blogPageSEO.objects.exists():
        blogPageSEO.objects.create(
            meta_title="Blogs",
            meta_description="The CodeGrammer",
            language=default_language
        )
        print("Blog Page SEO created.")
    else:
        print("Blog Page SEO already exists. Skipping creation.")