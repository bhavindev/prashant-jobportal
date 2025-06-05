from django.urls import path
from apps.aboutpage.views import *

urlpatterns = [
    path('about-us/', aboutPage, name='aboutUS'),
    path('team/detail/<str:slug>', teamSigngle, name='teamSigngle'),
]
