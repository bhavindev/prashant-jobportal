from django.shortcuts import render, redirect, get_object_or_404
from apps.custompage.models import customPage
from apps.custompage.forms import customPageForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from apps.lang.models import Languages
from django.urls import reverse

# Admin Custom Page Views
@login_required(login_url='logIn')
def adminCustomPage(request):
    
    default_language = Languages.objects.filter(is_default=True).first()
    default_language_code = default_language.code if default_language else None
    
    pages = customPage.objects.filter(language__code=default_language_code)
    
    language_code = request.GET.get('language')
    
    if language_code:
        pages = customPage.objects.filter(language__code=language_code)

    context = {
        'pages': pages, 
        'title': 'All Custom Pages',
        'all_languages': Languages.objects.all(),
        'selected_language': language_code,  
        'default_language_code': default_language_code,
        }
    return render(request, 'admin/front/main/custompage/index.html', context)

@login_required(login_url='logIn')
def adminCustomPageCreate(request):    
    default_language = Languages.objects.filter(is_default=True).first()
    default_language_code = default_language.code if default_language else None
    
    language_code = request.GET.get('language')
    
    if request.method == 'POST':
        form = customPageForm(request.POST)
        if form.is_valid():
            page = form.save(commit=False)
            page.language = Languages.objects.get(code=language_code)
            page.save()
            messages.success(request, 'Page created successfully!')
            return redirect(reverse('adminCustomPage') + f'?language={language_code}')
    else:
        form = customPageForm()
        
    context = {
        'form': form, 
        'title': 'Create Page',
        'all_languages': Languages.objects.all(),
        'selected_language': language_code,  
        'default_language_code': default_language_code,
        }
    return render(request, 'admin/front/main/custompage/create.html', context)

@login_required(login_url='logIn')
def adminCustomPageEdit(request, slug):
    page = get_object_or_404(customPage, slug=slug)
    if request.method == 'POST':
        form = customPageForm(request.POST, instance=page)
        if form.is_valid():
            form.save()
            messages.success(request, 'Page updated successfully!')
            return redirect(reverse('adminCustomPage') + f'?language={page.language.code}')
    else:
        form = customPageForm(instance=page)
        
    context = {
        'form': form, 
        'title': 'Create Page',
        'page': page,
        }
    
    return render(request, 'admin/front/main/custompage/edit.html', context)
    
@login_required(login_url='logIn')
def adminCustomPageDelete(request,id):
    page = get_object_or_404(customPage, id=id)
    messages.warning(request, 'Page deleted successfully!')
    page.delete()
    return redirect('adminCustomPage')

# Custom Page Front
def customPageFront(request, slug):
    # Get the default language
    default_language = Languages.objects.filter(is_default=True).first()
    
    # Get the selected language from session or use default language
    selected_language_code = request.session.get('selected_language', default_language.code)

    page = get_object_or_404(customPage, slug=slug)
    
    current_page_position = customPage.objects.filter(language=page.language, id__lt=page.id).count() + 1
    
    # Handle language selection from dropdown
    if request.method == 'POST':
        try:
            selected_language_code = request.POST.get('language', default_language.code)
            request.session['selected_language'] = selected_language_code
            
            selected_language_page = customPage.objects.filter(language__code=selected_language_code)[current_page_position - 1]
            if selected_language_page:
                return redirect('customPageFront', slug=selected_language_page.slug)
        except:
            messages.warning(request, 'Something went wrong! Translation not available for this page.')
        
    return render(request, 'front/main/partials/custom_page.html', {'page': page})
    
# Error Page
def error_404(request, exception):
    return render(request, 'error/404.html', status=404)

def error_500(request):
    return render(request, 'error/500.html', status=500)