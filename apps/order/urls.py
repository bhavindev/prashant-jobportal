from django.urls import path
from apps.order.views import *
from apps.order.sslcommerze_pay import *
from apps.order.paypal import *
from apps.order.stripe import *
from apps.order.razorpay import *
from apps.order.instamojo import *
from apps.order.paymob import *

urlpatterns = [
    path('user/products/', product_list, name='product_list'),
    path('cart/add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('user/cart/delete/<int:id>/', cart_delete, name='cart_delete'),
    path('user/cart/', view_cart, name='view_cart'),
    path('user/checkout/', checkout, name='checkout'),
    path('order/confirmation/<int:id>/', order_confirmation, name='order_confirmation'),
    path('order/payment-failed', payment_failed, name='payment_failed'),
    
    

    path('order/sslcommerze/success', sslcommerze_success, name='sslcommerz_success'),
    path('order/sslcommerze/failed', sslcommerze_failed, name='sslcommerz_failed'),

    path('order/paypal/success', paypal_success, name='paypal_success'),
    path('order/paypal/failed', paypal_failed, name='paypal_failed'),

    path('order/stripe/success', stripe_success, name='stripe_success'),
    
    path('order/instamojo/success', instamojo_success, name='instamojo_success'),
    path('order/instamojo/failed', instamojo_failed, name='instamojo_failed'),
    
    path('order/paymob/success', paymob_success, name='paymob_success'),
    # Example in urls.py
    # path('order/razorpay/getaway/<int:price>/', razorpayGetaway, name='razorpay_getaway'),

    # path('order/razorpay/success/', razorpay_success, name='razorpay_success'),

]
