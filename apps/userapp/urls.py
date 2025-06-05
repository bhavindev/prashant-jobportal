from django.urls import path
from apps.userapp.views import *
from apps.userapp.sslcommerze import *
from apps.userapp.paypal import *
from apps.userapp.instamojo import *
from apps.userapp.stripe import *

urlpatterns = [
    
    # User Home
    path('user/dashboard', userDashboard, name='userDashboard'),
    
    # User Ticket URLS
    path('user/dashboard/tickets', ticketList, name='userTickets'),
    path('user/dashboard/ticket/create/', userTicketCreate, name='userTicketCreate'),
    path('user/dashboard/ticket/view/<int:id>', userticketView, name='userticketView'),
    path('user/dashboard/delete/ticket/<int:id>', userTicketDelete , name='userTicketDelete'),

    # User Project URLS
    path('user/dashboard/projects', userProjects, name='userProjects'),
    path('user/dashboard/project/details/<slug:slug>', projectDetail, name='userProjectDetail'),
    
    # User Invoice URLS
    path('user/dashboard/invoices' ,userInvoices, name='userInvoices'),
    path('user/dashboard/invoice/view/<slug:slug>', viewUserPDFInvoice, name='viewUserPDFInvoice'),
    
    # User Payments URLS
    path('user/dashboard/payments', userPayments, name='userPayments'),
    
    # User Profile URLS
    path('user/dashboard/profile', customUserProfile, name='customUserProfile'),
    path('user/dashboard/profile/edit/', profile_edit_view, name='profile_edit'),
    
    # User Agreement URLS
    path('user/dashboard/agreements', userAgreements, name='userAgreements'),
    path('user/dashboard/agreement/view/<int:id>', userAgreementDetail, name='userAgreementDetail'),
    
    # User Orders
    path('user/dashboard/orders', userOrders, name='userOrders'),
    path('user/dashboard/order/<str:order_id>', userOrderDetail, name='userOrderDetail'),
    
    # Invoice payment
    path('payment/confirmation/<slug:slug>/', inv_payment_confirmation, name='inv_payment_confirmation'),
    path('payment/payment-failed/', inv_payment_failed, name='inv_payment_failed'),

    # SSLCOMMERZ
    path('invoice/sslcommerze/success/', inv_sslc_success, name='inv_sslc_success'),
    path('invoice/sslcommerze/failed/', inv_sslc_failed, name='inv_sslc_failed'),
    
    # PayPal
    path('invoice/paypal/success/', inv_paypal_success, name='inv_paypal_success'),
    path('invoice/paypal/failed/', inv_paypal_failed, name='inv_paypal_failed'),
    
    # Instamojo
    path('invoice/instamojo/success/', inv_instamojo_success, name='inv_instamojo_success'),
    
    # Stripe
    path('invoice/stripe/success', inv_stripe_success, name='inv_stripe_success'),
]
