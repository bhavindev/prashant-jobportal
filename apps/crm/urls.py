from django.urls import path
from apps.crm.views import *
from apps.order.admin_dash import *

urlpatterns = [
    path('admin/crm/home', crmHome, name='crmHome'),
    
    # Item URLS
    path('admin/crm/items', crmItems, name='crmItems'),
    path('admin/crm/item/create', crmItemCreate, name='crmItemCreate'),
    path('admin/crm/item/edit/<str:slug>/', crmItemEdit, name='crmItemEdit'),
    path('admin/crm/item/delete/<slug:slug>/', crmItemDelete, name='crmItemDelete'),
    
    # Item Category URLS
    path('admin/crm/item/categories', crmItemCategory, name='crmItemCategories'),
    path('admin/crm/item/category/create', crmItemCategoryCreate, name='crmItemCategoryCreate'),
    path('admin/crm/item/category/edit/<slug:slug>', crmItemCategoryEdit, name='crmItemCategoryEdit'),
    path('admin/crm/item/category/delete/<slug:slug>', crmItemCategoryDelete, name='crmItemCategoryDelete'),
    
    # CRM Clients URLS
    path('admin/crm/clients', crmClientsList, name='crmClients'),
    path('admin/crm/client/create', crmClientCreate, name='crmClientCreate'),
    path('admin/crm/client/edit/<slug:slug>', crmClientEdit, name='crmClientEdit'),
    path('admin/crm/client/delete/<slug:slug>', crmClientDelete, name='crmClientDelete'),
    
    # CRM Projects URLS
    path('admin/crm/projects', crmProjectsList, name='crmProjects'),
    path('admin/crm/project/create', crmProjectCreate, name='crmProjectCreate'),
    path('admin/crm/project/edit/<slug:slug>', crmProjectEdit, name='crmProjectEdit'),
    path('admin/crm/project/delete/<slug:slug>', crmProjectDelete, name='crmProjectDelete'),
    
    # CRM Tasks URLS
    path('admin/crm/tasks', crmTasksList, name='crmTasks'),
    path('admin/crm/task/done/<int:id>', taskmarkDone, name='taskmarkDone'),
    path('admin/crm/task/create', crmTaskCreate, name='crmTaskCreate'),
    path('admin/crm/task/edit/<int:id>', crmTaskEdit, name='crmTaskEdit'),
    path('admin/crm/task/delete/<int:id>', crmTaskDelete, name='crmTaskDelete'),
    
    # CRM Invoice URLS
    path('admin/crm/invoices', invoiceList, name='crmInvoiceList'),
    path('admin/crm/invoice/create', createInvoice, name='crmInvoiceCreate'),
    path('admin/crm/invoice/<slug:slug>',createBuildInvoice, name='create-build-invoice'),
    path('admin/crm/invoice/delete/<slug:slug>', deleteInvoice, name='deleteInvoice'),
    path('admin/crm/invoice/<slug:slug>/delete/product/<int:product_id>/', delete_invoice_product, name='delete-invoice-product'),
    
    #PDF Invoice
    path('admin/crm/invoice/view/<slug:slug>', viewPrintnvoice, name='viewPrintnvoice'),
    
    # CRM Payment URLS
    path('admin/crm/payments', paymentsList, name='payments'),
    path('admin/crm/payment/create', paymentCreate, name='paymentCreate'),
    path('admin/crm/payment/edit/<slug:slug>', paymentEdit, name='paymentEdit'),
    path('admin/crm/payment/delete/<slug:slug>', paymentDelete, name='paymentDelete'),
    
    # CRM Expense URLS
    path('admin/crm/expenses', expensesList, name='expenses'),
    path('admin/crm/expense/create', expenseCreate, name='expenseCreate'),
    path('admin/crm/expense/edit/<slug:slug>/', expenseEdit, name='expenseEdit'),
    path('admin/crm/expense/delete/<slug:slug>/', expenseDelete, name='expenseDelete'),
    
    # CRM Ticket URLS
    path('admin/crm/support-tickets', ticketList, name='tickets'),
    path('admin/crm/ticket/view/<int:id>', ticketView, name='ticketView'),
    path('admin/crm/ticket/delete/<int:id>', adminTicketDelete, name='adminTicketDelete'),
    path('ticket/reply/<int:id>', TicketReply, name='TicketReply'),

    # Order Admin URL
    path('admin/crm/orders', adminAllOrders, name='adminAllOrders'),
    path('admin/crm/pending-orders', adminPendingOrders, name='adminPendingOrders'),
    path('admin/crm/confirmed-orders', adminConfirmedOrders, name='adminConfirmedOrders'),
    path('admin/crm/completed-orders', adminCompletedOrders, name='adminCompletedOrders'),
    path('admin/crm/canceled-orders', adminCanceledOrders, name='adminCanceledOrders'),
    path('admin/crm/promo-codes', adminPromoCodes, name='adminPromoCodes'),
    path('admin/crm/promo-code/edit/<int:id>', adminPromoCodeEdit, name='adminPromoCodeEdit'),
    path('admin/crm/promo-code/delete/<int:id>', adminPromoCodeDelete, name='adminPromoCodeDelete'),
    
    # Order Details
    path('admin/crm/order/<int:user>/<str:order_id>', adminOrderDetails, name='adminOrderDetails'),
    
    # Order Delete
    path('admin/crm/order/delete/<str:order_id>', adminOrderDelete, name='adminOrderDelete'),

]
