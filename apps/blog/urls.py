from django.urls import path
from apps.blog.views import *

urlpatterns = [
    path('blogs/', blogHomeFront,name='blogs'),
    path('blog/<str:slug>', blogDetailPage, name='blogDetail')
]
