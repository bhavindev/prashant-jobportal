from django.urls import path 
from apps.custompage.views import *

urlpatterns = [
    path('admin/custom-pages/', adminCustomPage, name='adminCustomPage'),
    path('admin/create/custom-page/', adminCustomPageCreate, name='adminCustomPageCreate'),
    path('admin/custom-pages/edit/<str:slug>', adminCustomPageEdit, name='adminCustomPageEdit'),
    path('admin/custom-page/<int:id>/delete/', adminCustomPageDelete, name='adminCustomPageDelete'),
    
    path('<str:slug>/', customPageFront, name='customPageFront')
]
