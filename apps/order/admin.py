from django.contrib import admin
from apps.order.models import Order, Cart, PromoCode

admin.site.register(Order)
admin.site.register(Cart)
admin.site.register(PromoCode)