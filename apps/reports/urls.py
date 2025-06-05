from django.urls import path
from apps.reports.views import *

urlpatterns = [
    # CRM Profit Loss Report
    path('admin/crm/reports/profit-loss-report/', profitLossReport, name='profitLossReport'),
    path('admin/crm/reports/this-year-profit-loss/print/', thisYearProfitLossPrint, name='thisYearProfitLossPrint'),
    path('admin/crm/reports/this-month-profit-loss/print/', thisMonthProfitLossPrint, name='thisMonthProfitLossPrint'),
    path('admin/crm/reports/previous-year-profit-loss/print/', previousYearProfitLossPrint, name='previousYearProfitLossPrint'),
    path('admin/crm/reports/all-time-profit-loss/print/', allTimeProfitLossPrint, name='allTimeProfitLossPrint'),
    
    # CRM Payments Report
    path('admin/crm/reports/payments-report/', paymentsReport, name='paymentsReport'),
    
    # CRM Expense Report
    path('admin/crm/reports/expenses-report/', expenseReport, name='expenseReport'),
    
    # CRM Clients Report
    path('admin/crm/reports/clients-report/', clientsReport, name='clientsReport'),
        
    # CRM Invoice Report
    path('admin/crm/reports/invoice-report/', invoiceReport, name='invoiceReport'),
    path('admin/crm/reports/print/invoice/this-year', invoicePrintThisYear, name='invoicePrintThisYear'),
    path('admin/crm/reports/print/invoice/this-month', invoicePrintThisMonth, name='invoicePrintThisMonth'),
    path('admin/crm/reports/print/invoice/previous-year', invoicePrintPrevYear, name='invoicePrintPrevYear'),
    path('admin/crm/reports/print/invoice/all-time', invoicePrintAllTime, name='invoicePrintAllTime'),
    
    # CRM Project Report
    path('admin/crm/reports/project-report/', projectReport, name='projectReport'),
    
    # CRM Orders Report
    path('admin/crm/reports/order-reports/', adminOrderReport, name='adminOrderReport'),
    path('admin/crm/reports/print/order/all-time', printAllTimeOrders, name='printAllTimeOrders'),
    path('admin/crm/reports/print/order/this-year', printThisYearOrders, name='printThisYearOrders'),
    path('admin/crm/reports/print/order/this-month', printThisMonthOrders, name='printThisMonthOrders'),
    path('admin/crm/reports/print/order/previous-year', printPrevYearOrders, name='printPrevYearOrders'),
    
    # CRM Activity Log Report
    path('admin/crm/reports/activity-logs-report/', activityLogReport, name='activityLogReport'),
    
    # User Reports
    
    # User invoice report
    path('user/reports/invoice-report/', userInvoiceReport, name='userInvoiceReport'),
    path('user/reports/print/invoice/this-year/', userInvoicePrintThisYear, name='userInvoicePrintThisYear'),
    path('user/reports/print/invoice/this-month/', userInvoicePrintThisMonth, name='userInvoicePrintThisMonth'),
    path('user/reports/print/invoice/previous-year/', userInvoicePrintPrevYear, name='userInvoicePrintPrevYear'),
    path('user/reports/print/invoice/all-time/', userInvoicePrintAllTime, name='userInvoicePrintAllTime'),
    
    # User project report
    path('user/reports/project-report/', userProjectReport, name='userProjectReport'),
    
    # User payment report
    path('user/reports/payment-report/', userPaymentsReport, name='userPaymentsReport'),
    
]
