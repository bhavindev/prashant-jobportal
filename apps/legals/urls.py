from django.urls import path
from apps.legals.views import *

urlpatterns = [
    # Legal Admin URLS
    path('admin/pages/edit/t&C', termsPageAdmin , name='termsPageAdmin'),
    path('admin/pages/edit/privacy-policy', policyPageAdmin , name='policyPageAdmin'),
    
    # Legal Front URLS
    path('terms-conditions/', termsPageFront, name='termsPageFront'),
    path('privacy-policy/', policyPageFront, name='policyPageFront'),
    
]
