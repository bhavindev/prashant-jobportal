from django.shortcuts import render, redirect
from apps.homepage.models import serviceSection, funFactSection, funFactSectionTitle, serviceSectionTitle
from apps.aboutpage.models import clientsSection
from apps.servicepage.models import *
from apps.lang.models import Languages

def servicePage(request):
    # Get the default language
    default_language = Languages.objects.filter(is_default=True).first()
    
    # Get the selected language from session or use default language
    selected_language_code = request.session.get('selected_language', default_language.code)
    
    meta = ServicePageSEO.objects.filter(language__code=selected_language_code).first()
    
    services = serviceSection.objects.filter(language__code=selected_language_code)
    service_section_title = serviceSectionTitle.objects.filter(language__code=selected_language_code).first()
    
    # Handle language selection from dropdown
    if request.method == 'POST':
        selected_language_code = request.POST.get('language', default_language.code)
        request.session['selected_language'] = selected_language_code
        return redirect('frontServicePage')
    
    context = {
        'meta' : meta,
        
        'services' : services,
        'service_section_title' : service_section_title,
    }
    return render(request, 'front/main/services.html', context)

# Error Page
def error_404(request, exception):
    return render(request, 'error/error_404.html', status=404)