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
def create_banner_section(sender, **kwargs):
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
        default_language = Languages.objects.get(is_default=True)
    except Languages.DoesNotExist:
        default_language = Languages.objects.create(name="English", code="en", is_default=True)
        print("Default language (English) created.")

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

    if not bannerSection.objects.exists():
        with open(image_path, 'rb') as f:
            banner_section = bannerSection.objects.create(
                title="Welcome to The CodeGrammer",
                description="Lorem ipsum dolor sit amet consectetur adipisicing elit. Quo quasi adipisci magni reprehenderit quidem perspiciatis ullam fugit optio eligendi deserunt.",
                button_text="View Projects",
                button_url="#",
                show_quote_form=True,
                quote_form_title="Get a free Keystroke quote now",
                quote_form_field1_title="Name",
                quote_form_field1_placeholder="Your name",
                quote_form_field2_title="Email",
                quote_form_field2_placeholder="example@gmail.com",
                quote_form_field3_title="Phone",
                quote_form_field3_placeholder="+123456789",
                quote_form_button_text="submit",
                language=default_language,
            )
            banner_section.background_image.save(image_name, File(f))
            print("Default bannerSection created with background image.")
    else:
        print("bannerSection already exists. Skipping creation.")

@receiver(post_migrate)
def create_service_sections(sender, **kwargs):
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
        default_language = Languages.objects.get(is_default=True)
    except Languages.DoesNotExist:
        default_language = Languages.objects.create(name="English", code="en", is_default=True)

    # Create serviceSectionTitle data
    if not serviceSectionTitle.objects.exists():
        serviceSectionTitle.objects.create(
            title_small="What We Can Do For You",
            title_big="Services we can <br>help you with",
            service_card_more_text="Read More",
            language=default_language
        )
        print("Service section title created.")
    else:
        print("Service section title already exists. Skipping creation.")

    # Create serviceSection data
    if not serviceSection.objects.exists():
        services = [
            {
                "title": "Web Development",
                "description": "<p>Your design has to be as intuitive as it is helpful and insightful. In the dozen years, we’ve been in this industry, we gathered an intimate understanding of the latest UI & UX behaviors.</p>",
                "image_url": "https://crm.thecodegrammer.net/media/Home_images/icon-1.png",
                "order": 1
                
            },
            {
                "title": "App development",
                "description": "<p>Mobile app development is the act or process by which a mobile app is developed for mobile devices, such as personal digital assistants, enterprise digital assistants or mobile phone.</p>",
                "image_url": "https://crm.thecodegrammer.net/media/Home_images/icon-32.png",
                "order": 2
            },
            {
                "title": "SEO Solutions",
                "description": "<p>There’s some SEO in everything you do online. But that doesn’t mean everyone needs the same SEO services. Build your search engine optimization foundation with the trusted experts.</p>",
                "image_url": "https://crm.thecodegrammer.net/media/Home_images/icon-34.png",
                "order": 3
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
                    language=default_language
                )
                service_record.image.save(image_name, File(f))
                print(f"Service section '{service['title']}' created with image.")
    else:
        print(f"Service section already exists. Skipping creation.")
            
            
@receiver(post_migrate)
def create_project_sections(sender, **kwargs):
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
        default_language = Languages.objects.get(is_default=True)
    except Languages.DoesNotExist:
        default_language = Languages.objects.create(name="English", code="en", is_default=True)

    # Create projectSectionTitle data
    if not projectSectionTitle.objects.exists():
        projectSectionTitle.objects.create(
            title_small="Our Project",
            title_big="Some of our <br> finest work.",
            all_work_text="All Works",
            language=default_language
        )
        print("Project section title created.")
    else:
        print("Project section title already exists. Skipping creation.")

    # Create projectCategory data and fetch instances
    categories = {
        "eCommerce": None,
        "LMS": None,
        "Magazine": None
    }

    for cat_title in categories:
        category, created = projectCategory.objects.get_or_create(
            title=cat_title,
            language=default_language,
            defaults={"slug": cat_title.lower().replace(" ", "-")}
        )
        categories[cat_title] = category
        if created:
            print(f"Project category '{cat_title}' created.")
        else:
            print(f"Project category '{cat_title}' already exists. Skipping creation.")

    # Create projectsSection data
    if not projectsSection.objects.exists():
        projects = [
            {
                "title": "Multivendor eCommerce",
                "category": "eCommerce",
                "image_url": "https://crm.thecodegrammer.net/media/Home_images/1.jpg",
                "description": """
                    <p><strong>Lorem ipsum dolor</strong></p>
                    <p>sit amet consectetur, adipisicing elit. Rem earum magnam, non quos ipsum in tenetur doloremque maxime quam...</p>
                """,
                "client": "Emart",
                "duration": "3 Days",
                "button_text": "View website",
                "button_url": "#",
                "order": 1
            },
            {
                "title": "Ultimate School Management",
                "category": "LMS",
                "image_url": "https://crm.thecodegrammer.net/media/Home_images/2.png",
                "description": """
                    <p><strong>Lorem ipsum dolor</strong></p>
                    <p>sit amet consectetur, adipisicing elit. Rem earum magnam, non quos ipsum in tenetur doloremque maxime quam...</p>
                """,
                "client": "Rino",
                "duration": "3 Days",
                "button_text": "View website",
                "button_url": "#",
                "order": 2
            },
            {
                "title": "News Portal Magazine Web",
                "category": "Magazine",
                "image_url": "https://crm.thecodegrammer.net/media/Home_images/3.png",
                "description": """
                    <p><strong>Lorem ipsum dolor</strong></p>
                    <p>sit amet consectetur, adipisicing elit. Rem earum magnam, non quos ipsum in tenetur doloremque maxime quam...</p>
                """,
                "client": "Mega",
                "duration": "3 Days",
                "button_text": "View website",
                "button_url": "#",
                "order": 3
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
                    language=default_language
                )
                project_record.image.save(image_name, File(f))
                print(f"Project '{project['title']}' created with image.")
    else:
        print(f"Project already exists. Skipping creation.")
            
@receiver(post_migrate)
def create_fun_facts(sender, **kwargs):
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

    # Get the default language
    try:
        default_language = Languages.objects.get(is_default=True)
    except Languages.DoesNotExist:
        default_language = Languages.objects.create(name="English", code="en", is_default=True)

    # Check if any record exists in funFactSection and funFactSectionTitle
    if not funFactSection.objects.exists():
        # Fun facts to create
        fun_facts = [
            {"fact_count": "125", "title": "Happy Customers"},
            {"fact_count": "208", "title": "Projects"},
            {"fact_count": "15", "title": "Running Project"},
            {"fact_count": "100", "title": "Clients Satisfaction"},
        ]

        # Create funFactSection entries
        for fact in fun_facts:
            funFactSection.objects.create(
                fact_count=fact["fact_count"],
                title=fact["title"],
                language=default_language
            )
        print("Fun facts created.")
    else:
        print("Fun facts already exist. Skipping creation.")

    # Check if any record exists in funFactSectionTitle
    if not funFactSectionTitle.objects.exists():
        funFactSectionTitle.objects.create(
            title_small="Fun Facts",
            title_big="Our Achievements",
            language=default_language
        )
        print("Fun fact section title created.")
    else:
        print("Fun fact section title already exists. Skipping creation.")
        
        
@receiver(post_migrate)
def create_testimonials(sender, **kwargs):
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

    # Get the default language
    try:
        default_language = Languages.objects.get(is_default=True)
    except Languages.DoesNotExist:
        default_language = Languages.objects.create(name="English", code="en", is_default=True)

    # Check if any record exists in testimonialSectionTitle
    if not testimonialSectionTitle.objects.exists():
        testimonialSectionTitle.objects.create(
            title_small="Testimonial",
            title_big="From getting started",
            language=default_language
        )
        print("Testimonial section title created.")
    else:
        print("Testimonial section title already exists. Skipping creation.")

    # Check if any record exists in testimonialsSection
    if not testimonialsSection.objects.exists():
        testimonials = [
            {
                "title": "P Digital",
                "client_name": "Shakib",
                "client_designation": "CEO",
                "description": "They worked with me in two projects: one for my agency and another for my eCommerce. Both are best what they have given me.",
                "language": default_language
            },
            {
                "title": "A Aromas",
                "client_name": "Kashif",
                "client_designation": "CEO",
                "description": "They are so good. The CodeGrammer provided my project on time for my eCommerce website. Satisfied with their work.",
                "language": default_language
            },
            {
                "title": "The ABS",
                "client_name": "Mira Tabassum",
                "client_designation": "CEO",
                "description": "The CodeGrammer is a wonderful company. They are always on time, pleasant, and produce great work.",
                "language": default_language
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
        print("Testimonials created.")
    else:
        print("Testimonials already exist. Skipping creation.")
        
        
@receiver(post_migrate)
def create_home_page_seo(sender, **kwargs):
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

    # Get the default language
    try:
        default_language = Languages.objects.get(is_default=True)
    except Languages.DoesNotExist:
        print("Default language not found.")
        return

    # Check if any record exists in HomePageSEO
    if not HomePageSEO.objects.exists():
        HomePageSEO.objects.create(
            meta_title="The CodeGrammer",
            meta_description="Best Web & Application developer",
            language=default_language
        )
        print("Home Page SEO created.")
    else:
        print("Home Page SEO already exists. Skipping creation.")
        
@receiver(post_migrate)
def create_blog_section_title(sender, **kwargs):
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
        default_language = Languages.objects.get(is_default=True)
    except Languages.DoesNotExist:
        default_language = Languages.objects.create(name="English", code="en", is_default=True)

    if not blogSectionTitle.objects.exists():
        blogSectionTitle.objects.create(
            title_small="Blogs",
            title_big="Our Latest News",
            language=default_language
        )
        print("Blog section title created.")
    else:
        print("Blog section title already exists. Skipping creation.")
