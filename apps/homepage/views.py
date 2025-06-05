from django.shortcuts import render, redirect
from apps.homepage.models import *
from apps.aboutpage.models import *
from apps.blog.models import *
from django.utils import timezone
from datetime import datetime
from django.http import JsonResponse
from apps.adminapp.forms import ContactForm
from django.views.decorators.csrf import csrf_exempt
from apps.analytics.utils import visitor_data
from apps.lang.models import Languages
from apps.contactpage.models import *
from apps.custompage.models import *
from apps.portfoliopage.models import *
from apps.pricingpage.models import *
from apps.servicepage.models import *
from apps.settings.models import *
from django.core.paginator import Paginator

# Front Home Page
def language_assign(request):
    
    default_language = Languages.objects.filter(is_default=True).first()
            
    # language assignment for existing data without language
    models_to_update = [
        HomePageSEO, bannerSection, serviceSection, projectsSection,
        projectCategory, funFactSection, testimonialsSection,
        blogs, clientsSection, serviceSectionTitle,
        projectSectionTitle, funFactSectionTitle,
        testimonialSectionTitle, clientSectionTitle,
        blogSectionTitle, teamSection, teamSectionTitle, aboutSettings, AboutPageSEO,
        blogPageSEO, blogCategory, ContactInfo, ContactPageSEO, customPage,
        PortfolioPageSEO, 
        pricing, pricingPageSEO, pricingSectionTitle,
        ServicePageSEO,
        websiteSetting, SeoSetting, Menu, HeaderFooter,
        
    ]
    
    for model in models_to_update:
        objects_without_language = model.objects.filter(language=None)
        
        if objects_without_language.exists():
            for obj in objects_without_language:
                obj.language = default_language
                obj.save()

@csrf_exempt
def homePage(request):
    visitor_data(request)
    
    try:
        default_language = Languages.objects.filter(is_default=True).first()
        if not default_language:
            default_language = Languages.objects.first()
            default_language.is_default = True
            default_language.save()
    except:
        default_language = Languages.objects.create(
            name='English',
            code='en',
            is_default=True
        )
    
    # Get the selected language from session or use default language
    selected_language_code = request.session.get('selected_language', default_language.code)
    
    # Filter data based on the selected language
    meta = HomePageSEO.objects.filter(language__code=selected_language_code).first()
    banner = bannerSection.objects.filter(language__code=selected_language_code).first()
    service_sections = serviceSection.objects.filter(language__code=selected_language_code).order_by('order')
    projects_sections = projectsSection.objects.filter(language__code=selected_language_code).order_by('order')
    project_categories = projectCategory.objects.filter(language__code=selected_language_code)
    fun_fact_sections = funFactSection.objects.filter(language__code=selected_language_code)
    testimonials_sections = testimonialsSection.objects.filter(language__code=selected_language_code)
    blogs_section = blogs.objects.filter(language__code=selected_language_code)
    clients = clientsSection.objects.filter(language__code=selected_language_code)
    
    service_section_title = serviceSectionTitle.objects.filter(language__code=selected_language_code).first()
    project_section_title = projectSectionTitle.objects.filter(language__code=selected_language_code).first()
    fun_fact_section_title = funFactSectionTitle.objects.filter(language__code=selected_language_code).first()
    testimonials_section_title = testimonialSectionTitle.objects.filter(language__code=selected_language_code).first()
    client_section_title = clientSectionTitle.objects.filter(language__code=selected_language_code).first()
    blog_section_title = blogSectionTitle.objects.filter(language__code=selected_language_code).first()
    
    language_assign(request)
    
    # Handle language selection from dropdown
    if request.method == 'POST':
        selected_language_code = request.POST.get('language', default_language.code)
        request.session['selected_language'] = selected_language_code
        return redirect('homePage')
    
    context = {
        'meta': meta,
        'banner': banner,
        'services': service_sections,
        'projects': projects_sections,
        'project_categories': project_categories,
        'funfacts': fun_fact_sections,
        'blogs': blogs_section,
        'testimonials': testimonials_sections,
        'clients': clients,
        'selected_language_code': selected_language_code,
        'service_section_title': service_section_title,
        'project_section_title': project_section_title,
        'fun_fact_section_title': fun_fact_section_title,
        'testimonials_section_title': testimonials_section_title,
        'client_section_title': client_section_title,
        'blog_section_title': blog_section_title,
        
    }
    
    return render(request, 'front/main/index.html', context)


# # # # # # # # # # # # # # # # # #
    # Contact Submit #
# # # # # # # # # # # # # # # # # #
def QuoteSubmit(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # Check if there's a session variable for the last submission time
        last_submission_time_str = request.session.get('last_contact_submission_time')

        if last_submission_time_str:
            # Convert the stored time string back to a datetime object
            last_submission_time = datetime.fromisoformat(last_submission_time_str)

            # Calculate the time difference between the last submission and the current time
            time_difference = timezone.now() - last_submission_time

            # Check if less than five minutes have passed since the last submission
            if time_difference.total_seconds() < 300:  # 300 seconds = 5 minutes
                # Calculate the time left for the next submission
                time_left_seconds = 300 - time_difference.total_seconds()
                minutes_left = int(time_left_seconds / 60)
                seconds_left = int(time_left_seconds % 60)

                return JsonResponse({'status': 'error', 'message': f'You can submit again in {minutes_left} minutes and {seconds_left} seconds.'})

        # Save the current time in the session as a string in ISO 8601 format
        request.session['last_contact_submission_time'] = timezone.now().isoformat()

        form = ContactForm(request.POST)
        if form.is_valid():
            form.instance.message = 'This form is submitted from the get quote form'
            form.save()
            return JsonResponse({'status': 'success', 'message': 'Submitted successfully! We will get back to you soon.'})
        else:
            print(form.errors)
            return JsonResponse({'status': 'error', 'message': 'Invalid submit! Try again.'})

    return JsonResponse({'status': 'error', 'message': 'Invalid method or not an AJAX request!'})

def DynamicCss(request):
    
    if not Languages.objects.exists():
        Languages.objects.create(
            name='English',
            code='en',
            is_default=True
        )
    else:
        default_language = Languages.objects.filter(is_default=True).first()
        if not default_language:
            default_language = Languages.objects.first()
            default_language.is_default = True
            default_language.save()
    
    selected_language_code = request.session.get('selected_language', default_language.code)
    
    website_settings = websiteSetting.objects.filter(language__code=selected_language_code).first()
    
    context = {
        'primary_color': website_settings.primary_color if website_settings else '#5956E9',
        'link_color': website_settings.link_color if website_settings else '#2522BA',
        'wp_button_shed_color': website_settings.wp_button_shed_color if website_settings else '#6164FF66',
    }
    return render(request, 'front/styles.css', context, content_type='text/css')

def CombinedSearch(request):
    search_query = request.GET.get('search', '').strip()

    if search_query:
        default_language = Languages.objects.filter(is_default=True).first()
        selected_language_code = request.session.get('selected_language', default_language.code)
        
        services = serviceSection.objects.filter(title__icontains=search_query, language__code=selected_language_code)
        service_page_funfacts = funFactSection.objects.filter(language__code=selected_language_code)
        service_page_clients = clientsSection.objects.filter(language__code=selected_language_code)
        service_page_fun_fact_section_title = funFactSectionTitle.objects.filter(language__code=selected_language_code).first()
        service_page_service_section_title = serviceSectionTitle.objects.filter(language__code=selected_language_code).first()
        if services.exists():
            context = {
                'services': services,
                'search_query': search_query,
                'fun_fact_section_title': service_page_fun_fact_section_title,
                'service_section_title': service_page_service_section_title,
                'funfacts': service_page_funfacts,
                'clients': service_page_clients,
                'meta': ServicePageSEO.objects.filter(language__code=selected_language_code).first(),
            }
            return render(request, 'front/main/services.html', context)

        projects = projectsSection.objects.filter(title__icontains=search_query, language__code=selected_language_code)
        project_project_section_title = projectSectionTitle.objects.filter(language__code=selected_language_code).first()
        if projects.exists():
            context = {
                'projects': projects,
                'search_query': search_query,
                'project_section_title': project_project_section_title,
                'meta': PortfolioPageSEO.objects.filter(language__code=selected_language_code).first(),
            }
            return render(request, 'front/main/projects.html', context)

        list_blogs = blogs.objects.filter(title__icontains=search_query, language__code=selected_language_code)
        if list_blogs.exists():
            paginator = Paginator(list_blogs, 3) 
            page = request.GET.get('page')
            all_blogs = paginator.get_page(page)
            context = {
                'blogs': all_blogs,
                'search_query': search_query,
                'meta': blogPageSEO.objects.filter(language__code=selected_language_code).first(),
            }
            return render(request, 'front/main/blog.html', context)

    # If nothing is found, return 404 page
    return render(request, 'error/error_404.html', status=404)


# Error Page
def error_404(request, exception):
    return render(request, 'error/error_404.html', status=404)