from django.shortcuts import render, get_object_or_404, redirect
from apps.homepage.models import projectsSection, projectCategory, projectSectionTitle
from apps.portfoliopage.models import PortfolioPageSEO
from apps.lang.models import Languages
from django.contrib import messages


def projectPage(request):
    # Get the default language
    default_language = Languages.objects.filter(is_default=True).first()
    
    # Get the selected language from session or use default language
    selected_language_code = request.session.get('selected_language', default_language.code)
    
    meta = PortfolioPageSEO.objects.filter(language__code=selected_language_code).first()
    
    projects = projectsSection.objects.filter(language__code=selected_language_code).order_by('id')
    categories = projectCategory.objects.filter(language__code=selected_language_code).all()
    project_section_title = projectSectionTitle.objects.filter(language__code=selected_language_code).first()
    
    # Handle language selection from dropdown
    if request.method == 'POST':
        selected_language_code = request.POST.get('language', default_language.code)
        request.session['selected_language'] = selected_language_code
        return redirect('frontProjectPage')
    
    context = {
        'meta' : meta,
        'projects' : projects,
        'project_categories' : categories,
        'project_section_title' : project_section_title,
    }
    return render(request, 'front/main/projects.html', context)

def projectDetailPage(request, slug):
    # Get the default language
    default_language = Languages.objects.filter(is_default=True).first()
    
    # Get the selected language from session or use default language
    selected_language_code = request.session.get('selected_language', default_language.code)
    project = get_object_or_404(projectsSection, slug=slug)
    
    current_page_position = projectsSection.objects.filter(language=project.language, id__lt=project.id).count() + 1
    
    # Handle language selection from dropdown
    if request.method == 'POST':
        try:
            selected_language_code = request.POST.get('language', default_language.code)
            request.session['selected_language'] = selected_language_code
            
            selected_language_page = projectsSection.objects.filter(language__code=selected_language_code)[current_page_position - 1]
            if selected_language_page:
                return redirect('projectDetail', slug=selected_language_page.slug)
        except:
            messages.warning(request, 'Something went wrong! Translation not available for this project.')
    context = {
        'title' : 'Projects',
        'project' : project
    }
    return render(request, 'front/main/partials/project_details.html', context)

# Error Page
def error_404(request, exception):
    return render(request, 'error/error_404.html', status=404)