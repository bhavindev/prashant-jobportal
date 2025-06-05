from django.urls import path
from apps.servicepage.views import servicePage

urlpatterns = [
    path('services/', servicePage, name='frontServicePage' )
]
