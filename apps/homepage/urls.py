from django.urls import path
from apps.homepage.views import *

urlpatterns = [
    path('', homePage, name='homePage'),
    path('ajax-quote/', QuoteSubmit, name='QuoteSubmit'),
    path('styles.css', DynamicCss, name='front_styles'),
    
    path('search/', CombinedSearch, name='combined_search'),
]
