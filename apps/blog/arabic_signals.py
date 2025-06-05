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
def create_arabic_blogs_and_categories(sender, **kwargs):
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

    # Get the Arabic language
    try:
        arabic_language = Languages.objects.get(code="ar")
    except Languages.DoesNotExist:
        arabic_language = Languages.objects.create(name="Arabic", code="ar", is_rtl=True)

    # Create Arabic blog categories if they don't exist
    categories_data = [
        {"title": "الأعمال", "language": arabic_language},
        {"title": "التعليم", "language": arabic_language},
    ]

    categories = {}

    for category_data in categories_data:
        category, created = blogCategory.objects.get_or_create(
            title=category_data["title"],
            defaults={"language": category_data["language"]}
        )
        categories[category_data["title"]] = category
        if created:
            print(f"Arabic Category '{category_data['title']}' created.")
        else:
            print(f"Arabic Category '{category_data['title']}' already exists. Skipping creation.")

    # Check if any Arabic blogs exist
    if not blogs.objects.filter(language=arabic_language).exists():
        # Arabic blog data
        blog_entries = [
            {
                "thumbnail_url": "https://crm.thecodegrammer.net/media/blogs/1.jpg",
                "title": "The CodeGrammer : قوة الابتكار الرقمي",
                "category": categories["الأعمال"],  # Set the correct foreign key for category
                "description": """
                    <p><strong>تعظيم وصولك باستخدام التجارة على فيسبوك</strong><br />
                    التجارة على فيسبوك، أو ما يعرف بـ"ف-كوميرس"، هو إجراء الأنشطة التجارية عبر صفحة فيسبوك الخاصة بالشركة. ويشمل ذلك بيع وشراء المنتجات والخدمات مباشرة على منصة التواصل الاجتماعي. مع أكثر من 2.8 مليار مستخدم نشط شهريًا، أصبح فيسبوك أداة قوية للشركات للوصول إلى جمهورها المستهدف.</p>

                    <p>في The CodeGrammer، نؤمن بأن التجارة على فيسبوك هي مكون أساسي لأي استراتيجية تجارة إلكترونية ناجحة. واحدة من أهم مزايا ف-كوميرس هي القدرة على الوصول إلى جمهور واسع ومتنوع. مع أكثر من 2.8 مليار مستخدم نشط شهريًا، يسمح فيسبوك للشركات باستهداف الديموغرافيات المحددة، مثل العمر والجنس والموقع، مما يجعل من الأسهل الوصول إلى العملاء المحتملين. بالإضافة إلى ذلك، يمكن للشركات استخدام التحليلات المدمجة في فيسبوك لتتبع المشاركة والتحويلات، مما يوفر رؤى قيمة حول أداء جهود ف-كوميرس الخاصة بهم.</p>
                """,
                "author": "The CodeGrammer",
                "language": arabic_language,
            },
            {
                "thumbnail_url": "https://crm.thecodegrammer.net/media/blogs/2.jpg",
                "title": "كل شيء عن خرافات بدء التشغيل في الأعمال",
                "category": categories["التعليم"],  # Set the correct foreign key for category
                "description": """
                    <p><strong>تعظيم وصولك باستخدام التجارة على فيسبوك</strong><br />
                    التجارة على فيسبوك، أو ما يعرف بـ"ف-كوميرس"، هو إجراء الأنشطة التجارية عبر صفحة فيسبوك الخاصة بالشركة. ويشمل ذلك بيع وشراء المنتجات والخدمات مباشرة على منصة التواصل الاجتماعي. مع أكثر من 2.8 مليار مستخدم نشط شهريًا، أصبح فيسبوك أداة قوية للشركات للوصول إلى جمهورها المستهدف.</p>

                    <p>في The CodeGrammer، نؤمن بأن التجارة على فيسبوك هي مكون أساسي لأي استراتيجية تجارة إلكترونية ناجحة. واحدة من أهم مزايا ف-كوميرس هي القدرة على الوصول إلى جمهور واسع ومتنوع. مع أكثر من 2.8 مليار مستخدم نشط شهريًا، يسمح فيسبوك للشركات باستهداف الديموغرافيات المحددة، مثل العمر والجنس والموقع، مما يجعل من الأسهل الوصول إلى العملاء المحتملين. بالإضافة إلى ذلك، يمكن للشركات استخدام التحليلات المدمجة في فيسبوك لتتبع المشاركة والتحويلات، مما يوفر رؤى قيمة حول أداء جهود ف-كوميرس الخاصة بهم.</p>
                """,
                "author": "The CodeGrammer",
                "language": arabic_language,
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
                print(f"Arabic Blog '{blog_data['title']}' created with thumbnail.")
    else:
        print("Arabic blogs already exist. Skipping creation.")


@receiver(post_migrate)
def create_arabic_blog_page_seo(sender, **kwargs):
    if sender.name != 'apps.blog':
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

    # Get the Arabic language
    try:
        arabic_language = Languages.objects.get(code="ar")
    except Languages.DoesNotExist:
        arabic_language = Languages.objects.create(name="Arabic", code="ar", is_rtl=True)

    # Check if any record exists in blogPageSEO
    if not blogPageSEO.objects.filter(language=arabic_language).exists():
        blogPageSEO.objects.create(
            meta_title="المدونات",
            meta_description="The CodeGrammer",
            language=arabic_language
        )
        print("Arabic Blog Page SEO created.")
    else:
        print("Arabic Blog Page SEO already exists. Skipping creation.")
