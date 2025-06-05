from django.urls import path
from apps.pricingpage.views import *

urlpatterns = [
    path('pricing/', pricingPage, name='pricingPage')
]
