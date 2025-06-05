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
def create_clients(sender, **kwargs):
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

    # Get the default language
    try:
        default_language = Languages.objects.get(is_default=True)
    except Languages.DoesNotExist:
        print("Default language not found.")
        return

    # Check if any record exists in clientSectionTitle
    if not clientSectionTitle.objects.exists():
        clientSectionTitle.objects.create(
            title_small="Top Clients",
            title_big="We’ve built solutions for...",
            language=default_language
        )
        print("Client section title created.")
    else:
        print("Client section title already exists. Skipping creation.")

    # Check if any record exists in clientsSection
    if not clientsSection.objects.exists():
        clients = [
            {
                "company_name": "Client 01",
                "company_url": "#",
                "image_url": "https://crm.thecodegrammer.net/media/clients/brand-1.png",
            },
            {
                "company_name": "Client 02",
                "company_url": "#",
                "image_url": "https://crm.thecodegrammer.net/media/clients/brand-2.png",
            },
            {
                "company_name": "Client 03",
                "company_url": "#",
                "image_url": "https://crm.thecodegrammer.net/media/clients/brand-3.png",
            },
            {
                "company_name": "Client 04",
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
                    language=default_language
                )
                client_record.image.save(image_name, File(f))
                print(f"Client '{client['company_name']}' created with image.")
    else:
        print("Clients already exist. Skipping creation.")



@receiver(post_migrate)
def create_about_settings(sender, **kwargs):
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

    # Get the default language
    try:
        default_language = Languages.objects.get(is_default=True)
    except Languages.DoesNotExist:
        default_language = Languages.objects.create(name="English", code="en", is_default=True)

    # Check if any record exists in aboutSettings
    if not aboutSettings.objects.exists():

        # Create the aboutSettings entry
        about_record = aboutSettings.objects.create(
            title_white="Welcome to",
            title_red="The CodeGrammer.",
            heading="Building software for world changers",
            description="""
                <p>Welcome to The CodeGrammer, a leading web and application development company dedicated to crafting tailored digital solutions that help businesses thrive in the fast-paced digital world. With a strong focus on innovation, creativity, and technical excellence, we specialize in delivering custom web applications and mobile solutions that meet the unique needs of each of our clients. Whether you&#39;re a small startup aiming to disrupt your industry or an established enterprise seeking to streamline operations, The CodeGrammer is your trusted partner in digital transformation.</p>

                <h3>Who We Are</h3>

                <p>At The CodeGrammer, we are a team of passionate developers, designers, and strategists with a deep understanding of cutting-edge technologies and industry best practices. With years of experience under our belt, we have honed our expertise in web and mobile application development, ensuring that each project we undertake is executed with precision and dedication.</p>

                <p>We believe in building more than just software; we believe in creating impactful digital experiences that help our clients achieve their business goals. Our solutions are designed to be scalable, secure, and user-friendly, ensuring seamless performance for businesses of all sizes and industries.</p>

                <h3>What We Do</h3>

                <p>At The CodeGrammer, our services span across a broad range of web and mobile development needs, including:</p>

                <ul>
                    <li>
                    <p><strong>Custom Web Applications</strong>: We design and develop high-performing web applications that are responsive, robust, and built to address your business-specific needs. Whether it&#39;s a complex enterprise system or a user-focused e-commerce platform, our custom web solutions ensure optimal functionality and a superior user experience.</p>
                    </li>
                    <li>
                    <p><strong>Mobile Application Development</strong>: In today&rsquo;s mobile-first world, having a high-quality mobile app is essential. Our team creates custom mobile applications for iOS and Android that are tailored to your business, offering sleek design, high performance, and seamless integration with your existing infrastructure.</p>
                    </li>
                    <li>
                    <p><strong>Full-Stack Development</strong>: From the front-end user experience to back-end system architecture, we provide full-stack development services that ensure your web or mobile app is both visually appealing and functionally robust. We work with a variety of frameworks and technologies, always using the best tools for the job.</p>
                    </li>
                    <li>
                    <p><strong>UI/UX Design</strong>: User experience is at the heart of every successful digital product. Our team of designers and UX experts work closely with you to create intuitive, engaging interfaces that not only look great but also provide a smooth and efficient user journey.</p>
                    </li>
                    <li>
                    <p><strong>API Integration &amp; Development</strong>: We create and integrate APIs to ensure seamless connectivity between your applications, databases, and third-party services, enabling better functionality and communication across platforms.</p>
                    </li>
                </ul>

                <h3>Our Approach</h3>

                <p>At The CodeGrammer, we follow a customer-centric approach, making sure that each solution we deliver aligns perfectly with our clients&rsquo; objectives. Our process is highly collaborative&mdash;starting with understanding your vision, followed by a detailed discovery phase, and then executing development with agility and transparency. We ensure timely delivery and post-launch support, so your digital product continues to evolve and perform at its best.</p>

                <h3>Why Choose The CodeGrammer?</h3>

                <ul>
                    <li>
                    <p><strong>Tailored Solutions</strong>: We understand that no two businesses are the same. That&rsquo;s why every project we undertake is customized to meet your unique requirements.</p>
                    </li>
                    <li>
                    <p><strong>Experienced Team</strong>: Our team brings a wealth of knowledge and expertise, having successfully completed projects across various industries, from healthcare to e-commerce, finance, education, and more.</p>
                    </li>
                    <li>
                    <p><strong>Cutting-Edge Technology</strong>: We leverage the latest technology stacks and frameworks to ensure that our solutions are future-proof, scalable, and secure.</p>
                    </li>
                    <li>
                    <p><strong>Customer Satisfaction</strong>: Our clients are our top priority. We pride ourselves on delivering solutions that exceed expectations, offering ongoing support, and building long-lasting relationships.</p>
                    </li>
                    <li>
                    <p><strong>Agile Development</strong>: We follow agile development methodologies, ensuring that your project is delivered on time, within budget, and with the flexibility to adapt as your needs evolve.</p>
                    </li>
                </ul>

                <h3>Our Mission</h3>

                <p>At The CodeGrammer, our mission is to empower businesses by delivering top-notch digital solutions that drive innovation, enhance productivity, and unlock new opportunities. We are committed to helping you navigate the complexities of today&rsquo;s digital landscape with confidence and success.</p>

                <h3>Let&rsquo;s Build Together</h3>

                <p>Whether you&rsquo;re looking to build a new web application, revamp your current digital platform, or launch a game-changing mobile app, The CodeGrammer is here to turn your ideas into reality. Let us help you take your business to the next level with custom solutions that deliver real results.</p>

                <p><strong>Contact us today</strong> to start your journey towards digital excellence with The CodeGrammer.</p>

            """,
            count_title1="Years on the market",
            years_of_experience=3,
            count_title2="Projects delivered so far",
            project_delivered=250,
            button_text="Contact us",
            button_url="/contact-us",
            language=default_language
        )
        print("About settings created with image.")
    else:
        print("About settings already exist. Skipping creation.")
        
        
@receiver(post_migrate)
def create_team_members_and_title(sender, **kwargs):
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

    # Get the default language
    try:
        default_language = Languages.objects.get(is_default=True)
    except Languages.DoesNotExist:
        default_language = Languages.objects.create(name="English", code="en", is_default=True)

    # Create teamSectionTitle if no record exists
    if not teamSectionTitle.objects.exists():
        teamSectionTitle.objects.create(
            title_small="Our values",
            title_big="Meet The Team",
            language=default_language
        )
        print("Team section title created.")
    else:
        print("Team section title already exists. Skipping creation.")

    # Check if any record exists in teamSection
    if not teamSection.objects.exists():
        team_members = [
            {
                "name": "Endrew Raiko",
                "about": "The CodeGrammer, led by Endrew Raiko, is a thriving community for coding enthusiasts. With Rakib's passion for technology, it's a place where innovation and learning thrive. Join us in shaping the future of coding and technology!",
                "position": "Founder & Director",
                "image_url": "https://crm.thecodegrammer.net/media/team/team-1.jpg",
            },
            {
                "name": "Alex Mairo",
                "about": "Meet Alex Mairo, a passionate [Interest or Field] enthusiast from [Hometown or Current Location]. Their [Highlight a Remarkable Skill or Trait] and dedication to [Relevant Field or Cause] are truly remarkable. Join us in welcoming Alex and sharing in their journey toward [Shared Goal or Vision]",
                "position": "Manager",
                "image_url": "https://crm.thecodegrammer.net/media/team/team-3.jpg",
            },
            {
                "name": "Thoren Okendhild",
                "about": "Meet Thoren Okendhild, a passionate [Interest or Field] enthusiast from [Hometown or Current Location]. Their [Highlight a Remarkable Skill or Trait] and dedication to [Relevant Field or Cause] are truly remarkable. Join us in welcoming Thoren and sharing in their journey toward [Shared Goal or Vision]",
                "position": "Developer",
                "image_url": "https://crm.thecodegrammer.net/media/team/team-1.jpg",
            },
            {
                "name": "Adrian Eodri",
                "about": "Meet Adrian Eodri, a passionate [Interest or Field] enthusiast from [Hometown or Current Location]. Their [Highlight a Remarkable Skill or Trait] and dedication to [Relevant Field or Cause] are truly remarkable. Join us in welcoming Adrian and sharing in their journey toward [Shared Goal or Vision]",
                "position": "Designer",
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
                    language=default_language
                )
                team_record.image.save(image_name, File(f))
                print(f"Team member '{member['name']}' created with image.")
    else:
        print("Team members already exist. Skipping creation.")
        
        

@receiver(post_migrate)
def create_about_page_seo(sender, **kwargs):
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

    # Get the default language
    try:
        default_language = Languages.objects.get(is_default=True)
    except Languages.DoesNotExist:
        print("Default language not found.")
        return

    # Check if any record exists in AboutPageSEO
    if not AboutPageSEO.objects.exists():
        AboutPageSEO.objects.create(
            meta_title="About Us",
            meta_description="The CodeGrammer",
            language=default_language
        )
        print("About Page SEO created.")
    else:
        print("About Page SEO already exists. Skipping creation.")