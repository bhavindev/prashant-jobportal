from django.shortcuts import render, redirect
from apps.pricingpage.models import *

def pricingPage(request):
    # Get the default language
    default_language = Languages.objects.filter(is_default=True).first()
    
    # Get the selected language from session or use default language
    selected_language_code = request.session.get('selected_language', default_language.code)
    
    meta = pricingPageSEO.objects.filter(language__code=selected_language_code).first()
    
    pricing_list = pricing.objects.filter(language__code=selected_language_code).all()
    
    pricing_section_title = pricingSectionTitle.objects.filter(language__code=selected_language_code).first()
    
    # Handle language selection from dropdown
    if request.method == 'POST':
        selected_language_code = request.POST.get('language', default_language.code)
        request.session['selected_language'] = selected_language_code
        return redirect('pricingPage')
    
    context ={
        'meta' : meta,
        'pricing_list' : pricing_list,
        'pricing_section_title' : pricing_section_title,
    }
    
    return render(request, 'front/main/pricing.html', context)

# Error Page
def error_404(request, exception):
    return render(request, 'error/error_404.html', status=404)