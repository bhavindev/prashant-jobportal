from django.contrib import admin
from django.urls import path ,include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from core.sitemaps import generate_sitemap

urlpatterns = [
    path('oldadmin/', admin.site.urls),
    path('admin/', RedirectView.as_view(pattern_name="signIn"), name='admin_redirect'),
    path('dashboard/', RedirectView.as_view(pattern_name="signIn"), name='user_redirect'),
    path('', include('apps.adminapp.urls')),
    path('', include('apps.userapp.urls')),
    path('', include('apps.homepage.urls')),
    path('', include('apps.aboutpage.urls')),
    path('', include('apps.servicepage.urls')),
    path('', include('apps.portfoliopage.urls')),
    path('', include('apps.blog.urls')),
    path('', include('apps.authapp.urls')),
    path('', include('apps.pricingpage.urls')),
    path('', include('apps.contactpage.urls')),
    path('', include('apps.legals.urls')),
    path('', include('apps.crm.urls')),
    path('', include('apps.hrm.urls')),
    path('', include('apps.reports.urls')),
    path('', include('apps.marketing.urls')),
    path('', include('apps.custompage.urls')),
    path('', include('apps.order.urls')),
    path('', include('apps.ai.urls')),
    path('', include('apps.lang.urls')),
    path('sitemap.xml', generate_sitemap, name='generate_sitemap'),
]

handler404 = 'apps.authapp.views.error_404'
handler404 = 'apps.adminapp.views.error_404'
handler404 = 'apps.crm.views.error_404'
handler404 = 'apps.userapp.views.error_404'
handler404 = 'apps.homepage.views.error_404'
handler404 = 'apps.servicepage.views.error_404'
handler404 = 'apps.portfoliopage.views.error_404'
handler404 = 'apps.contactpage.views.error_404'
handler404 = 'apps.aboutpage.views.error_404'
handler404 = 'apps.blog.views.error_404'
handler404 = 'apps.settings.views.error_404'
handler404 = 'apps.legals.views.error_404'
handler404 = 'apps.reports.views.error_404'
handler404 = 'apps.marketing.views.error_404'

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
   