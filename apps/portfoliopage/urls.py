from django.urls import path
from apps.portfoliopage.views import *

urlpatterns = [
    path('projects/', projectPage, name='frontProjectPage'),
    path('project/view/<str:slug>', projectDetailPage, name='projectDetail')
    
]
