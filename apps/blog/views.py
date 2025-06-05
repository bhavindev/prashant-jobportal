from django.shortcuts import render, get_object_or_404, redirect
from apps.blog.models import *
from django.core.paginator import Paginator
from apps.lang.models import Languages
from django.contrib import messages


def blogHomeFront(request):
    # Get the default language
    default_language = Languages.objects.filter(is_default=True).first()
    
    # Get the selected language from session or use default language
    selected_language_code = request.session.get('selected_language', default_language.code)
    
    search = request.GET.get('search')
    blog_list = blogs.objects.filter(language__code=selected_language_code).all()
    meta = blogPageSEO.objects.filter(language__code=selected_language_code).first()

    if search:
        blog_list = blog_list.filter(title__icontains=search, language__code=selected_language_code) 

    paginator = Paginator(blog_list, 3)
    page = request.GET.get('page')
    all_blogs = paginator.get_page(page)
    
    # Handle language selection from dropdown
    if request.method == 'POST':
        selected_language_code = request.POST.get('language', default_language.code)
        request.session['selected_language'] = selected_language_code
        return redirect('blogs')

    context = {
        'title': 'Blogs',
        'blogs': all_blogs,
        'search': search,
        'meta': meta,
    }
    return render(request, 'front/main/blog.html', context)


def blogDetailPage(request, slug):
    
    # Get the default language
    default_language = Languages.objects.filter(is_default=True).first()
    
    # Get the selected language from session or use default language
    selected_language_code = request.session.get('selected_language', default_language.code)
    
    blog_list = blogs.objects.filter(language__code=selected_language_code)
    
    blog = get_object_or_404(blogs, slug=slug)
    
    current_page_position = blogs.objects.filter(language=blog.language, id__lt=blog.id).count() + 1
    
    # Handle language selection from dropdown
    if request.method == 'POST':
        try:
            selected_language_code = request.POST.get('language', default_language.code)
            request.session['selected_language'] = selected_language_code
            
            selected_language_page = blogs.objects.filter(language__code=selected_language_code)[current_page_position - 1]
            if selected_language_page:
                return redirect('blogDetail', slug=selected_language_page.slug)
        except:
            messages.warning(request, 'Something went wrong! Translation not available for this blog.')
        
    context = {
        'blog' : blog,
        'blogs' : blog_list
    }
    return render(request, 'front/main/partials/blogsingle.html', context)

# Error Page
def error_404(request, exception):
    return render(request, 'error/error_404.html', status=404)
