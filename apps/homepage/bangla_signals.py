import os
import requests
from django.core.files import File
from django.conf import settings
from django.db import connection
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from apps.lang.models import Languages
from apps.homepage.models import *

@receiver(post_migrate)
def create_bangla_banner_section(sender, **kwargs):
    if sender.name != 'apps.homepage':
        return

    table_name = bannerSection._meta.db_table

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT EXISTS (
                SELECT 1 
                FROM information_schema.tables 
                WHERE table_name = %s
            );
        """, [table_name])
        table_exists = cursor.fetchone()[0]
        
    if not table_exists:
        print(f"Table {table_name} does not exist. Skipping bannerSection creation.")
        return

    try:
        bangla_language = Languages.objects.get(code="bn")
    except Languages.DoesNotExist:
        bangla_language = Languages.objects.create(name="Bangla", code="bn", is_rtl=False)
        print("Bangla language created.")

    image_url = 'https://crm.thecodegrammer.net/media/Home_images/banner-bg-1_RGprZkw.png'
    image_name = 'banner-bg-1_RGprZkw.png'
    image_dir = os.path.join(settings.MEDIA_ROOT, 'Home_images')
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
            return

    if not bannerSection.objects.filter(language=bangla_language).exists():
        with open(image_path, 'rb') as f:
            banner_section = bannerSection.objects.create(
                title="কোডগ্রামার এ আপনাকে স্বাগতম",
                description="লোরেম ইপসাম ডলার সিট আমেট, কনসেকটেটুর এডিপিসিং এলিট। কোয়াসি মাগনি রেপ্রেসেন্ট, কোয়াসি ইউরিট এসেন্ডি এলিগেন্ডি।",
                button_text="প্রকল্প দেখুন",
                button_url="#",
                show_quote_form=True,
                quote_form_title="ফ্রি কিস্ট্রোক কোট পান",
                quote_form_field1_title="নাম",
                quote_form_field1_placeholder="আপনার নাম",
                quote_form_field2_title="ইমেইল",
                quote_form_field2_placeholder="example@gmail.com",
                quote_form_field3_title="ফোন",
                quote_form_field3_placeholder="+৮৮০১xxxxxxxx",
                quote_form_button_text="জমা দিন",
                language=bangla_language,
            )
            banner_section.background_image.save(image_name, File(f))
            print("Bangla bannerSection created with background image.")
    else:
        print("Bangla bannerSection already exists. Skipping creation.")

@receiver(post_migrate)
def create_bangla_service_sections(sender, **kwargs):
    if sender.name != 'apps.homepage':
        return

    service_section_table = serviceSection._meta.db_table
    service_section_title_table = serviceSectionTitle._meta.db_table
    
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT EXISTS (
                SELECT 1 
                FROM information_schema.tables 
                WHERE table_name = %s
            );
        """, [service_section_table])
        service_section_exists = cursor.fetchone()[0]

        cursor.execute("""
            SELECT EXISTS (
                SELECT 1 
                FROM information_schema.tables 
                WHERE table_name = %s
            );
        """, [service_section_title_table])
        service_section_title_exists = cursor.fetchone()[0]

    if not service_section_exists:
        print(f"Table {service_section_table} does not exist. Skipping serviceSection creation.")
        return
    
    if not service_section_title_exists:
        print(f"Table {service_section_title_table} does not exist. Skipping serviceSectionTitle creation.")
        return

    try:
        bangla_language = Languages.objects.get(code="bn")
    except Languages.DoesNotExist:
        bangla_language = Languages.objects.create(name="Bangla", code="bn", is_rtl=False)

    # Create serviceSectionTitle data
    if not serviceSectionTitle.objects.filter(language=bangla_language).exists():
        serviceSectionTitle.objects.create(
            title_small="আপনার জন্য কি করতে পারি",
            title_big="আমাদের সেবাগুলো যা আমরা আপনাকে সহায়তা করতে পারি",
            service_card_more_text="আরও পড়ুন",
            language=bangla_language
        )
        print("Bangla service section title created.")
    else:
        print("Bangla service section title already exists. Skipping creation.")

    # Create serviceSection data
    if not serviceSection.objects.filter(language=bangla_language).exists():
        services = [
            {
                "title": "ওয়েব ডেভেলপমেন্ট",
                "description": "<p>আপনার ডিজাইন হতে হবে যতটা ইন্টারেক্টিভ ততটাই উপকারী। আমরা বছরগুলোতে ইউআই এবং ইউএক্স নিয়ে গভীর অভিজ্ঞতা অর্জন করেছি।</p>",
                "image_url": "https://crm.thecodegrammer.net/media/Home_images/icon-1.png",
                "order": 4
            },
            {
                "title": "অ্যাপ ডেভেলপমেন্ট",
                "description": "<p>মোবাইল অ্যাপ ডেভেলপমেন্ট হল এমন একটি প্রক্রিয়া যার মাধ্যমে মোবাইল ডিভাইসের জন্য অ্যাপ তৈরি করা হয়।</p>",
                "image_url": "https://crm.thecodegrammer.net/media/Home_images/icon-32.png",
                "order": 5
            },
            {
                "title": "এসইও সমাধান",
                "description": "<p>অনলাইনে আপনার প্রতিটি কর্মকাণ্ডে এসইও থাকে। কিন্তু এর মানে এই নয় যে সবার একই এসইও সেবা দরকার। আমাদের বিশেষজ্ঞদের সাহায্যে আপনার এসইও পরিকল্পনা তৈরি করুন।</p>",
                "image_url": "https://crm.thecodegrammer.net/media/Home_images/icon-34.png",
                "order": 6
            }
        ]

        for service in services:
            image_url = service["image_url"]
            image_name = os.path.basename(image_url)
            image_dir = os.path.join(settings.MEDIA_ROOT, 'Home_images')
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
                service_record = serviceSection.objects.create(
                    title=service["title"],
                    description=service["description"],
                    language=bangla_language
                )
                service_record.image.save(image_name, File(f))
                print(f"Service section '{service['title']}' created with image.")
    else:
        print(f"Bangla service section already exists. Skipping creation.")


@receiver(post_migrate)
def create_bangla_project_sections(sender, **kwargs):
    if sender.name != 'apps.homepage':
        return

    # Check if the necessary tables exist
    tables = {
        "projectsSection": projectsSection._meta.db_table,
        "projectCategory": projectCategory._meta.db_table,
        "projectSectionTitle": projectSectionTitle._meta.db_table
    }

    with connection.cursor() as cursor:
        for table_name in tables.values():
            cursor.execute(f"""
                SELECT EXISTS (
                    SELECT 1 
                    FROM information_schema.tables 
                    WHERE table_name = %s
                );
            """, [table_name])
            table_exists = cursor.fetchone()[0]
            if not table_exists:
                print(f"Table {table_name} does not exist. Skipping data creation.")
                return

    try:
        bangla_language = Languages.objects.get(code="bn")
    except Languages.DoesNotExist:
        bangla_language = Languages.objects.create(name="Bangla", code="bn", is_rtl=False)

    # Create projectSectionTitle data
    if not projectSectionTitle.objects.filter(language=bangla_language).exists():
        projectSectionTitle.objects.create(
            title_small="আমাদের প্রকল্প",
            title_big="কিছু চমৎকার কাজ যা আমরা করেছি",
            all_work_text="সব কাজ",
            language=bangla_language
        )
        print("Bangla project section title created.")
    else:
        print("Bangla project section title already exists. Skipping creation.")

    # Create projectCategory data and fetch instances
    categories = {
        "ই-কমার্স": None,
        "এলএমএস": None,
        "ম্যাগাজিন": None
    }

    for cat_title in categories:
        category, created = projectCategory.objects.get_or_create(
            title=cat_title,
            language=bangla_language,
            defaults={"slug": cat_title.lower().replace(" ", "-")}
        )
        categories[cat_title] = category
        if created:
            print(f"Bangla Project category '{cat_title}' created.")
        else:
            print(f"Bangla Project category '{cat_title}' already exists. Skipping creation.")

    # Create projectsSection data
    if not projectsSection.objects.filter(language=bangla_language).exists():
        projects = [
            {
                "title": "মাল্টিভেন্ডর ই-কমার্স",
                "category": "ই-কমার্স",
                "image_url": "https://crm.thecodegrammer.net/media/Home_images/1.jpg",
                "description": """
                    <p><strong>লোরেম ইপসাম ডলার</strong></p>
                    <p>কনসেকটেটুর অ্যাডিপিসিং এলিট। রেম ইয়ারাম ম্যাগনাম...</p>
                """,
                "client": "ইমার্ট",
                "duration": "৩ দিন",
                "button_text": "ওয়েবসাইট দেখুন",
                "button_url": "#",
                "order" : 4
            },
            {
                "title": "আলটিমেট স্কুল ম্যানেজমেন্ট",
                "category": "এলএমএস",
                "image_url": "https://crm.thecodegrammer.net/media/Home_images/2.png",
                "description": """
                    <p><strong>লোরেম ইপসাম ডলার</strong></p>
                    <p>কনসেকটেটুর অ্যাডিপিসিং এলিট। রেম ইয়ারাম ম্যাগনাম...</p>
                """,
                "client": "রিনো",
                "duration": "৩ দিন",
                "button_text": "ওয়েবসাইট দেখুন",
                "button_url": "#",
                "order" : 5
            },
            {
                "title": "নিউজ পোর্টাল ম্যাগাজিন ওয়েব",
                "category": "ম্যাগাজিন",
                "image_url": "https://crm.thecodegrammer.net/media/Home_images/3.png",
                "description": """
                    <p><strong>লোরেম ইপসাম ডলার</strong></p>
                    <p>কনসেকটেটুর অ্যাডিপিসিং এলিট। রেম ইয়ারাম ম্যাগনাম...</p>
                """,
                "client": "মেগা",
                "duration": "৩ দিন",
                "button_text": "ওয়েবসাইট দেখুন",
                "button_url": "#",
                "order" : 6
            }
        ]

        for project in projects:
            image_url = project["image_url"]
            image_name = os.path.basename(image_url)
            image_dir = os.path.join(settings.MEDIA_ROOT, 'Home_images')
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
                project_record = projectsSection.objects.create(
                    title=project["title"],
                    category=categories[project["category"]],
                    description=project["description"],
                    client=project["client"],
                    duration=project["duration"],
                    button_text=project["button_text"],
                    button_url=project["button_url"],
                    language=bangla_language
                )
                project_record.image.save(image_name, File(f))
                print(f"Bangla Project '{project['title']}' created with image.")
    else:
        print(f"Bangla Project already exists. Skipping creation.")


@receiver(post_migrate)
def create_bangla_fun_facts(sender, **kwargs):
    if sender.name != 'apps.homepage':
        return

    # Check if the funFactSection and funFactSectionTitle tables exist
    fun_fact_table_name = funFactSection._meta.db_table
    fun_fact_title_table_name = funFactSectionTitle._meta.db_table

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT EXISTS (
                SELECT 1 
                FROM information_schema.tables 
                WHERE table_name = %s
            );
        """, [fun_fact_table_name])
        fun_fact_table_exists = cursor.fetchone()[0]

        cursor.execute("""
            SELECT EXISTS (
                SELECT 1 
                FROM information_schema.tables 
                WHERE table_name = %s
            );
        """, [fun_fact_title_table_name])
        fun_fact_title_table_exists = cursor.fetchone()[0]

    if not fun_fact_table_exists or not fun_fact_title_table_exists:
        print(f"Fun fact or fun fact title tables do not exist. Skipping creation.")
        return

    # Get the Bangla language
    try:
        bangla_language = Languages.objects.get(code="bn")
    except Languages.DoesNotExist:
        bangla_language = Languages.objects.create(name="Bangla", code="bn", is_rtl=False)

    # Check if any record exists in funFactSection and funFactSectionTitle
    if not funFactSection.objects.filter(language=bangla_language).exists():
        # Fun facts to create
        fun_facts = [
            {"fact_count": "১২৫", "title": "সুখী গ্রাহক"},
            {"fact_count": "২০৮", "title": "প্রকল্প"},
            {"fact_count": "১৫", "title": "চলমান প্রকল্প"},
            {"fact_count": "১০০", "title": "গ্রাহক সন্তুষ্টি"},
        ]

        # Create funFactSection entries
        for fact in fun_facts:
            funFactSection.objects.create(
                fact_count=fact["fact_count"],
                title=fact["title"],
                language=bangla_language
            )
        print("Bangla fun facts created.")
    else:
        print("Bangla fun facts already exist. Skipping creation.")

    # Check if any record exists in funFactSectionTitle
    if not funFactSectionTitle.objects.filter(language=bangla_language).exists():
        funFactSectionTitle.objects.create(
            title_small="মজার তথ্য",
            title_big="আমাদের অর্জন",
            language=bangla_language
        )
        print("Bangla fun fact section title created.")
    else:
        print("Bangla fun fact section title already exists. Skipping creation.")


@receiver(post_migrate)
def create_bangla_testimonials(sender, **kwargs):
    if sender.name != 'apps.homepage':
        return

    # Check if the testimonialsSection and testimonialSectionTitle tables exist
    testimonial_table_name = testimonialsSection._meta.db_table
    testimonial_title_table_name = testimonialSectionTitle._meta.db_table

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT EXISTS (
                SELECT 1 
                FROM information_schema.tables 
                WHERE table_name = %s
            );
        """, [testimonial_table_name])
        testimonial_table_exists = cursor.fetchone()[0]

        cursor.execute("""
            SELECT EXISTS (
                SELECT 1 
                FROM information_schema.tables 
                WHERE table_name = %s
            );
        """, [testimonial_title_table_name])
        testimonial_title_table_exists = cursor.fetchone()[0]

    if not testimonial_table_exists or not testimonial_title_table_exists:
        print(f"Testimonial or testimonial title tables do not exist. Skipping creation.")
        return

    # Get the Bangla language
    try:
        bangla_language = Languages.objects.get(code="bn")
    except Languages.DoesNotExist:
        bangla_language = Languages.objects.create(name="Bangla", code="bn", is_rtl=False)

    # Check if any record exists in testimonialSectionTitle
    if not testimonialSectionTitle.objects.filter(language=bangla_language).exists():
        testimonialSectionTitle.objects.create(
            title_small="গ্রাহক পর্যালোচনা",
            title_big="শুরু থেকেই",
            language=bangla_language
        )
        print("Bangla testimonial section title created.")
    else:
        print("Bangla testimonial section title already exists. Skipping creation.")

    # Check if any record exists in testimonialsSection
    if not testimonialsSection.objects.filter(language=bangla_language).exists():
        testimonials = [
            {
                "title": "পি ডিজিটাল",
                "client_name": "শাকিব",
                "client_designation": "সিইও",
                "description": "আমার এজেন্সি এবং ই-কমার্স উভয়ের জন্যই তারা দুর্দান্ত কাজ করেছে।",
                "language": bangla_language
            },
            {
                "title": "এ অ্যারোমাস",
                "client_name": "কাশিফ",
                "client_designation": "সিইও",
                "description": "কোডগ্রামার আমার ই-কমার্স প্রকল্প সময়মত সরবরাহ করেছে। আমি তাদের কাজে সন্তুষ্ট।",
                "language": bangla_language
            },
            {
                "title": "দ্য এবিএস",
                "client_name": "মীরা তাবাসসুম",
                "client_designation": "সিইও",
                "description": "কোডগ্রামার একটি চমৎকার কোম্পানি। তারা সবসময় সময়মতো থাকে এবং তাদের কাজের মান অত্যন্ত ভালো।",
                "language": bangla_language
            }
        ]

        # Create testimonialsSection entries
        for testimonial in testimonials:
            testimonialsSection.objects.create(
                title=testimonial["title"],
                client_name=testimonial["client_name"],
                client_designation=testimonial["client_designation"],
                description=testimonial["description"],
                language=testimonial["language"]
            )
        print("Bangla testimonials created.")
    else:
        print("Bangla testimonials already exist. Skipping creation.")


@receiver(post_migrate)
def create_bangla_home_page_seo(sender, **kwargs):
    if sender.name != 'apps.homepage':
        return

    # Check if the HomePageSEO table exists
    seo_table_name = HomePageSEO._meta.db_table

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
        print(f"Table {seo_table_name} does not exist. Skipping HomePageSEO creation.")
        return

    # Get the Bangla language
    try:
        bangla_language = Languages.objects.get(code="bn")
    except Languages.DoesNotExist:
        bangla_language = Languages.objects.create(name="Bangla", code="bn", is_rtl=False)

    # Check if any record exists in HomePageSEO
    if not HomePageSEO.objects.filter(language=bangla_language).exists():
        HomePageSEO.objects.create(
            meta_title="কোডগ্রামার",
            meta_description="সেরা ওয়েব ও অ্যাপ্লিকেশন ডেভেলপার",
            language=bangla_language
        )
        print("Bangla Home Page SEO created.")
    else:
        print("Bangla Home Page SEO already exists. Skipping creation.")


@receiver(post_migrate)
def create_bangla_blog_section_title(sender, **kwargs):
    if sender.name != 'apps.homepage':
        return

    blog_title_table_name = blogSectionTitle._meta.db_table

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT EXISTS (
                SELECT 1 
                FROM information_schema.tables 
                WHERE table_name = %s
            );
        """, [blog_title_table_name])
        blog_title_table_exists = cursor.fetchone()[0]

    if not blog_title_table_exists:
        print(f"Table {blog_title_table_name} does not exist. Skipping blogSectionTitle creation.")
        return

    try:
        bangla_language = Languages.objects.get(code="bn")
    except Languages.DoesNotExist:
        bangla_language = Languages.objects.create(name="Bangla", code="bn", is_rtl=False)

    if not blogSectionTitle.objects.filter(language=bangla_language).exists():
        blogSectionTitle.objects.create(
            title_small="ব্লগ",
            title_big="আমাদের সর্বশেষ সংবাদ",
            language=bangla_language
        )
        print("Bangla blog section title created.")
    else:
        print("Bangla blog section title already exists. Skipping creation.")
