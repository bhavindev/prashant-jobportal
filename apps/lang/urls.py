from django.urls import path
from apps.lang.views import *

urlpatterns = [
    path('admin/languages', adminLanguageHome, name='adminLanguageHome'),
    path('admin/language/create', adminLanguageCreate, name='adminLanguageCreate'),
    path('admin/language/edit/<str:code>', adminLanguageEdit, name='adminLanguageEdit'),
    path('admin/language/delete/<str:code>', adminLanguageDelete, name='adminLanguageDelete')
]