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
def create_arabic_banner_section(sender, **kwargs):
    if sender.name != 'apps.homepage':
        return

    table_name = bannerSection._meta.db_table

    # Check if the bannerSection table exists
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

    # Try to get or create the Arabic language
    try:
        arabic_language = Languages.objects.get(code="ar")
    except Languages.DoesNotExist:
        arabic_language = Languages.objects.create(name="Arabic", code="ar", is_rtl=True)
        print("Arabic language created.")

    # Define the image details
    image_url = 'https://crm.thecodegrammer.net/media/Home_images/banner-bg-1_RGprZkw.png'
    image_name = 'banner-bg-1_RGprZkw.png'
    image_dir = os.path.join(settings.MEDIA_ROOT, 'Home_images')
    image_path = os.path.join(image_dir, image_name)

    # Ensure the image directory exists
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)

    # Download the image if it does not exist
    if not os.path.exists(image_path):
        response = requests.get(image_url)
        if response.status_code == 200:
            with open(image_path, 'wb') as f:
                f.write(response.content)
            print(f"Image {image_name} downloaded.")
        else:
            print(f"Failed to download image from {image_url}")
            return

    # Create the bannerSection in Arabic if it doesn't exist
    if not bannerSection.objects.filter(language=arabic_language).exists():
        with open(image_path, 'rb') as f:
            banner_section = bannerSection.objects.create(
                title="مرحبًا بك في The CodeGrammer",
                description="لوريم إيبسوم هو نص تجريبي يستخدم في صناعات الطباعة والتنضيد.",
                button_text="عرض المشاريع",
                button_url="#",
                show_quote_form=True,
                quote_form_title="احصل على عرض سعر مجاني الآن",
                quote_form_field1_title="الاسم",
                quote_form_field1_placeholder="اسمك",
                quote_form_field2_title="البريد الإلكتروني",
                quote_form_field2_placeholder="example@gmail.com",
                quote_form_field3_title="الهاتف",
                quote_form_field3_placeholder="+123456789",
                quote_form_button_text="إرسال",
                language=arabic_language,
            )
            banner_section.background_image.save(image_name, File(f))
            print("Arabic bannerSection created with background image.")
    else:
        print("Arabic bannerSection already exists. Skipping creation.")
        
        
        

@receiver(post_migrate)
def create_arabic_service_sections(sender, **kwargs):
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
        arabic_language = Languages.objects.get(code="ar")
    except Languages.DoesNotExist:
        arabic_language = Languages.objects.create(name="Arabic", code="ar", is_rtl=True)
        print("Arabic language created.")

    # Create Arabic serviceSectionTitle data
    if not serviceSectionTitle.objects.filter(language=arabic_language).exists():
        serviceSectionTitle.objects.create(
            title_small="ماذا يمكننا أن نفعل من أجلك",
            title_big="الخدمات التي يمكننا <br> مساعدتك بها",
            service_card_more_text="اقرأ المزيد",
            language=arabic_language
        )
        print("Arabic service section title created.")
    else:
        print("Arabic service section title already exists. Skipping creation.")

    # Create Arabic serviceSection data
    if not serviceSection.objects.filter(language=arabic_language).exists():
        services = [
            {
                "title": "تطوير الويب",
                "description": "<p>تصميمك يجب أن يكون بديهياً ومفيداً كما هو ملهم. في الاثنتي عشرة سنة التي كنا فيها في هذه الصناعة، اكتسبنا فهماً عميقاً لأحدث سلوكيات واجهة المستخدم وتجربة المستخدم.</p>",
                "image_url": "https://crm.thecodegrammer.net/media/Home_images/icon-1.png",
                "order": 7
            },
            {
                "title": "تطوير التطبيقات",
                "description": "<p>تطوير تطبيقات الجوال هو العملية التي يتم من خلالها تطوير تطبيق جوال للأجهزة المحمولة مثل الهواتف الذكية.</p>",
                "image_url": "https://crm.thecodegrammer.net/media/Home_images/icon-32.png",
                "order": 8
            },
            {
                "title": "حلول تحسين محركات البحث",
                "description": "<p>توجد بعض تقنيات تحسين محركات البحث في كل ما تفعله عبر الإنترنت. ولكن هذا لا يعني أن الجميع يحتاجون إلى نفس الخدمات.</p>",
                "image_url": "https://crm.thecodegrammer.net/media/Home_images/icon-34.png",
                "order": 9
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
                    language=arabic_language
                )
                service_record.image.save(image_name, File(f))
                print(f"Arabic service section '{service['title']}' created with image.")
    else:
        print(f"Arabic service section already exists. Skipping creation.")


@receiver(post_migrate)
def create_arabic_project_sections(sender, **kwargs):
    if sender.name != 'apps.homepage':
        return

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
        arabic_language = Languages.objects.get(code="ar")
    except Languages.DoesNotExist:
        arabic_language = Languages.objects.create(name="Arabic", code="ar", is_rtl=True)
        print("Arabic language created.")

    if not projectSectionTitle.objects.filter(language=arabic_language).exists():
        projectSectionTitle.objects.create(
            title_small="مشاريعنا",
            title_big="بعض من <br> أرقى أعمالنا.",
            all_work_text="كل الأعمال",
            language=arabic_language
        )
        print("Arabic project section title created.")
    else:
        print("Arabic project section title already exists. Skipping creation.")

    categories = {
        "eCommerce": None,
        "LMS": None,
        "Magazine": None
    }

    for cat_title in categories:
        category, created = projectCategory.objects.get_or_create(
            title=cat_title,
            language=arabic_language,
            defaults={"slug": cat_title.lower().replace(" ", "-")}
        )
        categories[cat_title] = category
        if created:
            print(f"Arabic project category '{cat_title}' created.")
        else:
            print(f"Arabic project category '{cat_title}' already exists. Skipping creation.")

    if not projectsSection.objects.filter(language=arabic_language).exists():
        projects = [
            {
                "title": "تجارة إلكترونية متعددة البائعين",
                "category": "eCommerce",
                "image_url": "https://crm.thecodegrammer.net/media/Home_images/1.jpg",
                "description": """
                    <p><strong>لوريم إيبسوم</strong></p>
                    <p>النص التجريبي الأكثر شهرة في العالم، يستخدم عادة كمثال للكتابة الجيدة.</p>
                """,
                "client": "إيمارت",
                "duration": "3 أيام",
                "button_text": "عرض الموقع",
                "button_url": "#",
                "order": 7
            },
            {
                "title": "إدارة المدرسة النهائية",
                "category": "LMS",
                "image_url": "https://crm.thecodegrammer.net/media/Home_images/2.png",
                "description": """
                    <p><strong>لوريم إيبسوم</strong></p>
                    <p>النص التجريبي الأكثر شهرة في العالم، يستخدم عادة كمثال للكتابة الجيدة.</p>
                """,
                "client": "رينو",
                "duration": "3 أيام",
                "button_text": "عرض الموقع",
                "button_url": "#",
                "order": 8
            },
            {
                "title": "بوابة المجلة الإخبارية",
                "category": "Magazine",
                "image_url": "https://crm.thecodegrammer.net/media/Home_images/3.png",
                "description": """
                    <p><strong>لوريم إيبسوم</strong></p>
                    <p>النص التجريبي الأكثر شهرة في العالم، يستخدم عادة كمثال للكتابة الجيدة.</p>
                """,
                "client": "ميجا",
                "duration": "3 أيام",
                "button_text": "عرض الموقع",
                "button_url": "#",
                "order": 9
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
                    language=arabic_language
                )
                project_record.image.save(image_name, File(f))
                print(f"Arabic project '{project['title']}' created with image.")
    else:
        print(f"Arabic project already exists. Skipping creation.")


@receiver(post_migrate)
def create_arabic_fun_facts(sender, **kwargs):
    if sender.name != 'apps.homepage':
        return

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

    try:
        arabic_language = Languages.objects.get(code="ar")
    except Languages.DoesNotExist:
        arabic_language = Languages.objects.create(name="Arabic", code="ar", is_rtl=True)

    if not funFactSection.objects.filter(language=arabic_language).exists():
        fun_facts = [
            {"fact_count": "125", "title": "عملاء سعداء"},
            {"fact_count": "208", "title": "مشاريع"},
            {"fact_count": "15", "title": "مشروع جاري"},
            {"fact_count": "100", "title": "رضا العملاء"}
        ]

        for fact in fun_facts:
            funFactSection.objects.create(
                fact_count=fact["fact_count"],
                title=fact["title"],
                language=arabic_language
            )
        print("Arabic fun facts created.")
    else:
        print("Arabic fun facts already exist. Skipping creation.")

    if not funFactSectionTitle.objects.filter(language=arabic_language).exists():
        funFactSectionTitle.objects.create(
            title_small="حقائق ممتعة",
            title_big="إنجازاتنا",
            language=arabic_language
        )
        print("Arabic fun fact section title created.")
    else:
        print("Arabic fun fact section title already exists. Skipping creation.")


@receiver(post_migrate)
def create_arabic_testimonials(sender, **kwargs):
    if sender.name != 'apps.homepage':
        return

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

    try:
        arabic_language = Languages.objects.get(code="ar")
    except Languages.DoesNotExist:
        arabic_language = Languages.objects.create(name="Arabic", code="ar", is_rtl=True)

    if not testimonialSectionTitle.objects.filter(language=arabic_language).exists():
        testimonialSectionTitle.objects.create(
            title_small="شهادة",
            title_big="منذ البداية",
            language=arabic_language
        )
        print("Arabic testimonial section title created.")
    else:
        print("Arabic testimonial section title already exists. Skipping creation.")

    if not testimonialsSection.objects.filter(language=arabic_language).exists():
        testimonials = [
            {
                "title": "بي ديجيتال",
                "client_name": "شكيب",
                "client_designation": "الرئيس التنفيذي",
                "description": "لقد عملوا معي في مشروعين. كلا المشروعين كانا الأفضل."
            },
            {
                "title": "أ أروماس",
                "client_name": "كاشف",
                "client_designation": "الرئيس التنفيذي",
                "description": "هم جيدون للغاية. قدمت الشركة مشروعي في الوقت المحدد."
            },
            {
                "title": "ذا أي بي إس",
                "client_name": "ميرا تبسم",
                "client_designation": "الرئيس التنفيذي",
                "description": "شركة رائعة. دائمًا ما يقدمون العمل في الوقت المحدد."
            }
        ]

        for testimonial in testimonials:
            testimonialsSection.objects.create(
                title=testimonial["title"],
                client_name=testimonial["client_name"],
                client_designation=testimonial["client_designation"],
                description=testimonial["description"],
                language=arabic_language
            )
        print("Arabic testimonials created.")
    else:
        print("Arabic testimonials already exist. Skipping creation.")


@receiver(post_migrate)
def create_arabic_home_page_seo(sender, **kwargs):
    if sender.name != 'apps.homepage':
        return

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

    try:
        arabic_language = Languages.objects.get(code="ar")
    except Languages.DoesNotExist:
        arabic_language = Languages.objects.create(name="Arabic", code="ar", is_rtl=True)

    if not HomePageSEO.objects.filter(language=arabic_language).exists():
        HomePageSEO.objects.create(
            meta_title="The CodeGrammer",
            meta_description="أفضل مطور تطبيقات ومواقع",
            language=arabic_language
        )
        print("Arabic Home Page SEO created.")
    else:
        print("Arabic Home Page SEO already exists. Skipping creation.")


@receiver(post_migrate)
def create_arabic_blog_section_title(sender, **kwargs):
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
        arabic_language = Languages.objects.get(code="ar")
    except Languages.DoesNotExist:
        arabic_language = Languages.objects.create(name="Arabic", code="ar", is_rtl=True)

    if not blogSectionTitle.objects.filter(language=arabic_language).exists():
        blogSectionTitle.objects.create(
            title_small="مدونات",
            title_big="أحدث الأخبار",
            language=arabic_language
        )
        print("Arabic blog section title created.")
    else:
        print("Arabic blog section title already exists. Skipping creation.")