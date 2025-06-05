from django.shortcuts import render, get_object_or_404, redirect
from apps.aboutpage.models import *
from apps.homepage.models import testimonialsSection, testimonialSectionTitle, clientSectionTitle
from apps.lang.models import Languages
from django.contrib import messages

def aboutPage(request):
    # Get the default language
    default_language = Languages.objects.filter(is_default=True).first()
    
    # Get the selected language from session or use default language
    selected_language_code = request.session.get('selected_language', default_language.code)
    
    meta = AboutPageSEO.objects.filter(language__code=selected_language_code).first()
    
    about = aboutSettings.objects.filter(language__code=selected_language_code).first()
    teams = teamSection.objects.filter(language__code=selected_language_code)
    testimonials = testimonialsSection.objects.filter(language__code=selected_language_code)
    clients = clientsSection.objects.filter(language__code=selected_language_code)
    
    team_section_title = teamSectionTitle.objects.filter(language__code=selected_language_code).first()
    testimonials_section_title = testimonialSectionTitle.objects.filter(language__code=selected_language_code).first()
    client_section_title = clientSectionTitle.objects.filter(language__code=selected_language_code).first()
    
    # Handle language selection from dropdown
    if request.method == 'POST':
        selected_language_code = request.POST.get('language', default_language.code)
        request.session['selected_language'] = selected_language_code
        return redirect('aboutUS')
    
    context = {
        'meta' : meta,
        'about' : about,
        'teams' : teams.order_by('id'),
        'testimonials' : testimonials,
        'clients' : clients,
        'selected_language_code': selected_language_code,
        'team_section_title': team_section_title,
        'testimonials_section_title': testimonials_section_title,
        'client_section_title': client_section_title
    }
    return render(request, 'front/main/about.html', context)

def teamSigngle(request, slug):
    # Get the default language
    default_language = Languages.objects.filter(is_default=True).first()
    
    # Get the selected language from session or use default language
    selected_language_code = request.session.get('selected_language', default_language.code)
    
    team = get_object_or_404(teamSection, slug=slug)
    
    current_page_position = teamSection.objects.filter(language=team.language, id__lt=team.id).count() + 1
    
    # Handle language selection from dropdown
    if request.method == 'POST':
        try:
            selected_language_code = request.POST.get('language', default_language.code)
            request.session['selected_language'] = selected_language_code
            
            selected_language_page = teamSection.objects.filter(language__code=selected_language_code)[current_page_position - 1]
            if selected_language_page:
                return redirect('teamSigngle', slug=selected_language_page.slug)
        except:
            messages.warning(request, 'Something went wrong! Translation not available for this memeber.')
            
    context = {
        'team' : team
    }
    
    return render(request, 'front/main/partials/team_single.html', context)

# Error Page
def error_404(request, exception):
    return render(request, 'error/error_404.html', status=404)