from django.urls import path
from apps.contactpage.views import contactPageFront, ajax_subscribe , subscriberViewAdmin, subscriberDelete

urlpatterns = [
    path('contact-us/', contactPageFront, name='contactPageFront'),
    path('ajax_subscribe/', ajax_subscribe, name='ajax_subscribe'),
    path('admin/subscribers', subscriberViewAdmin, name='subscriberViewAdmin'),
    path('admin/subscriber/delete/<int:id>', subscriberDelete, name='subscriberDelete'),
]
