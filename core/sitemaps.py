from django.http import HttpResponse
from django.template import loader
from apps.homepage.models import projectsSection
from apps.aboutpage.models import teamSection
from apps.blog.models import blogs

def generate_sitemap(request):
    apps = [
        'homepage',
        'aboutpage',
        'servicepage',
        'portfoliopage',
        'blog',
        'pricingpage',
    ]

    urls = ['/',]

    for app_name in apps:
        try:
            urlconf = __import__(f'{app_name}.urls', fromlist=['urlpatterns'])
            urlpatterns = getattr(urlconf, 'urlpatterns', [])

            # Extract URL patterns from the resolver
            for pattern in urlpatterns:
                if hasattr(pattern, 'url_patterns'):
                    # If it's an included namespace, extract its URL patterns
                    urls.extend([f'/{url.pattern}' for url in pattern.url_patterns])
                else:
                    # Otherwise, add the URL pattern itself
                    urls.append(f'/{pattern.pattern}')
        except ImportError:
            pass

    # Add URLs for the Project model
    project_slugs = projectsSection.objects.values_list('slug', flat=True)
    if project_slugs:
        for slug in project_slugs:
            project_url = f'/project/view/{slug}/'
            urls.append(project_url)

    # Add URLs for the Blog model
    blog_slugs = blogs.objects.values_list('slug', flat=True)
    if blog_slugs:
        for slug in blog_slugs:
            blog_url = f'/blog/{slug}/'
            urls.append(blog_url)
        
    # Add URLs for the Team model
    team_id = teamSection.objects.values_list('id', flat=True)
    if team_id:
        for id in team_id:
            team_url = f'/team/detail/{id}/'
            urls.append(team_url)

    # Filter out the unwanted URLs with placeholders
    urls = [url for url in urls if '<slug:slug>' not in url and '<int:id>' not in url]
    

    context = {
        'urls': urls,
        'request': request,
    }

    sitemap_xml = loader.render_to_string('sitemap/sitemap.xml', context)
    sitemap_xml = sitemap_xml.replace('<priority>0.8</priority>', '<priority>1.0</priority>', 1)


    return HttpResponse(sitemap_xml, content_type="application/xml")
