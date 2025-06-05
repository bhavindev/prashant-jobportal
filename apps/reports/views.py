from django.shortcuts import render
from django.utils import timezone
from django.contrib.admin.models import LogEntry
from apps.crm.models import *
from apps.authapp.models import *
from core.decorators import admin_manager_role_required
from django.contrib.auth.decorators import login_required
from apps.order.models import Order

# Profit Loss Print
@login_required(login_url='signIn')
@admin_manager_role_required
def thisYearProfitLossPrint(request):
    current_year = timezone.now().year
    current_month = timezone.now().month
    previous_year = current_year - 1
    
    # This year payment
    payments_for_current_year = Payments.objects.filter(payment_date__year=current_year)
    current_year_total_payment = payments_for_current_year.aggregate(Sum('payment_ammount'))['payment_ammount__sum'] or 0
    
    payments_for_current_month = Payments.objects.filter(payment_date__year=current_year, payment_date__month=current_month)
    current_month_total_payment = payments_for_current_month.aggregate(Sum('payment_ammount'))['payment_ammount__sum'] or 0

    payments_for_previous_year = Payments.objects.filter(payment_date__year=previous_year)
    previous_year_total_payment = payments_for_previous_year.aggregate(Sum('payment_ammount'))['payment_ammount__sum'] or 0
    
    # This year expense
    expenses_for_current_year = Expense.objects.filter(date_of_expense__year=current_year)
    current_year_total_expense = expenses_for_current_year.aggregate(Sum('amount'))['amount__sum'] or 0
    
    # Calculate the total discount_amount, tax_amount, and other_fees_amount for the current year
    invoices_for_current_year = Invoice.objects.filter(billDate__year=current_year)
    current_year_total_discount = invoices_for_current_year.aggregate(Sum('discount_amount'))['discount_amount__sum'] or 0
    current_year_total_tax = invoices_for_current_year.aggregate(Sum('tax_amount'))['tax_amount__sum'] or 0
    current_year_total_other_fees = invoices_for_current_year.aggregate(Sum('other_fees_amount'))['other_fees_amount__sum'] or 0
    
    # This year calculation
    gross_profit_this_year = current_year_total_payment-current_year_total_expense
    net_profit_this_year = gross_profit_this_year-(current_year_total_discount+current_year_total_tax+current_year_total_other_fees)
    
    context = {
        'title' : f'{current_year} Profit & Loss Report',
        'gross_profit_this_year' : gross_profit_this_year,
        'net_profit_this_year' : net_profit_this_year,
        'current_year_total_payment' : current_year_total_payment,
        'current_month_total_payment' : current_month_total_payment,
        'previous_year_total_payment' : previous_year_total_payment,
        'current_year_total_expense' : current_year_total_expense,
        'current_year_total_discount' : current_year_total_discount,
        'current_year_total_tax' : current_year_total_tax,
        'current_year_total_other_fees' : current_year_total_other_fees
    }
    return render(request, 'crm/main/reports/partials/ThisYearPF/profit_loss_print.html', context)

@login_required(login_url='signIn')
@admin_manager_role_required
def thisMonthProfitLossPrint(request):
    current_year = timezone.now().year
    current_month = timezone.now().month
    previous_year = current_year - 1
    
    # Payments/Revenue Times
    payments_for_current_month = Payments.objects.filter(payment_date__year=current_year, payment_date__month=current_month)
    current_month_total_payment = payments_for_current_month.aggregate(Sum('payment_ammount'))['payment_ammount__sum'] or 0

    payments_for_previous_year = Payments.objects.filter(payment_date__year=previous_year)
    previous_year_total_payment = payments_for_previous_year.aggregate(Sum('payment_ammount'))['payment_ammount__sum'] or 0

    payments_for_current_year = Payments.objects.filter(payment_date__year=current_year)
    current_year_total_payment = payments_for_current_year.aggregate(Sum('payment_ammount'))['payment_ammount__sum'] or 0
    
    # Expense Times
    expenses_for_current_month = Expense.objects.filter(date_of_expense__year=current_year, date_of_expense__month=current_month)
    current_month_total_expense = expenses_for_current_month.aggregate(Sum('amount'))['amount__sum'] or 0
    
    # Calculate the total discount_amount, tax_amount, and other_fees_amount for the current month
    invoices_for_current_month = Invoice.objects.filter(billDate__year=current_year, billDate__month=current_month)
    current_month_total_discount = invoices_for_current_month.aggregate(Sum('discount_amount'))['discount_amount__sum'] or 0
    current_month_total_tax = invoices_for_current_month.aggregate(Sum('tax_amount'))['tax_amount__sum'] or 0
    current_month_total_other_fees = invoices_for_current_month.aggregate(Sum('other_fees_amount'))['other_fees_amount__sum'] or 0
    
    # This month calculation
    gross_profit_this_month = current_month_total_payment-current_month_total_expense
    net_profit_this_month = gross_profit_this_month-(current_month_total_discount+current_month_total_tax+current_month_total_other_fees)
    
    context = {
        'title' : f'{current_month}/{current_year} Profit & Loss Report',
        'gross_profit_this_month' : gross_profit_this_month,
        'net_profit_this_month' : net_profit_this_month,
        'current_year_total_payment' : current_year_total_payment,
        'current_month_total_payment' : current_month_total_payment,
        'previous_year_total_payment' : previous_year_total_payment,
        'current_month_total_expense' : current_month_total_expense,
        'current_month_total_discount' : current_month_total_discount,
        'current_month_total_tax' : current_month_total_tax,
        'current_month_total_other_fees' : current_month_total_other_fees
    }
    return render(request, 'crm/main/reports/partials/ThisMonthPF/profit_loss_print.html', context)

@login_required(login_url='signIn')
@admin_manager_role_required
def previousYearProfitLossPrint(request):
    current_year = timezone.now().year
    current_month = timezone.now().month
    previous_year = current_year - 1
    
    # Payments/Revenue Times
    payments_for_current_month = Payments.objects.filter(payment_date__year=current_year, payment_date__month=current_month)
    current_month_total_payment = payments_for_current_month.aggregate(Sum('payment_ammount'))['payment_ammount__sum'] or 0

    payments_for_previous_year = Payments.objects.filter(payment_date__year=previous_year)
    previous_year_total_payment = payments_for_previous_year.aggregate(Sum('payment_ammount'))['payment_ammount__sum'] or 0

    payments_for_current_year = Payments.objects.filter(payment_date__year=current_year)
    current_year_total_payment = payments_for_current_year.aggregate(Sum('payment_ammount'))['payment_ammount__sum'] or 0
    
    # Expense Times
    expenses_for_previous_year = Expense.objects.filter(date_of_expense__year=previous_year)
    previous_year_total_expense = expenses_for_previous_year.aggregate(Sum('amount'))['amount__sum'] or 0
    
    # Calculate the total discount_amount, tax_amount, and other_fees_amount for the previous year
    invoices_for_previous_year = Invoice.objects.filter(billDate__year=previous_year)
    previous_year_total_discount = invoices_for_previous_year.aggregate(Sum('discount_amount'))['discount_amount__sum'] or 0
    previous_year_total_tax = invoices_for_previous_year.aggregate(Sum('tax_amount'))['tax_amount__sum'] or 0
    previous_year_total_other_fees = invoices_for_previous_year.aggregate(Sum('other_fees_amount'))['other_fees_amount__sum'] or 0
    
    # previous year calculation
    gross_profit_previous_year = previous_year_total_payment-previous_year_total_expense
    net_profit_previous_year = gross_profit_previous_year-(previous_year_total_discount+previous_year_total_tax+previous_year_total_other_fees)
    
    context = {
        'title' : f'{previous_year} Profit & Loss Report',
        'gross_profit_previous_year' : gross_profit_previous_year,
        'net_profit_previous_year' : net_profit_previous_year,
        'current_year_total_payment' : current_year_total_payment,
        'current_month_total_payment' : current_month_total_payment,
        'previous_year_total_payment' : previous_year_total_payment,
        'previous_year_total_expense' : previous_year_total_expense,
        'previous_year_total_discount' : previous_year_total_discount,
        'previous_year_total_tax' : previous_year_total_tax,
        'previous_year_total_other_fees' : previous_year_total_other_fees
    }
    return render(request, 'crm/main/reports/partials/PreviousYearPF/profit_loss_print.html', context)

@login_required(login_url='signIn')
@admin_manager_role_required
def allTimeProfitLossPrint(request):
    current_year = timezone.now().year
    current_month = timezone.now().month
    previous_year = current_year - 1

    # Payments/Revenue Times
    payments_for_current_month = Payments.objects.filter(payment_date__year=current_year, payment_date__month=current_month)
    current_month_total_payment = payments_for_current_month.aggregate(Sum('payment_ammount'))['payment_ammount__sum'] or 0

    payments_for_previous_year = Payments.objects.filter(payment_date__year=previous_year)
    previous_year_total_payment = payments_for_previous_year.aggregate(Sum('payment_ammount'))['payment_ammount__sum'] or 0

    payments_for_current_year = Payments.objects.filter(payment_date__year=current_year)
    current_year_total_payment = payments_for_current_year.aggregate(Sum('payment_ammount'))['payment_ammount__sum'] or 0
    
    # All time
    total_revenue = Payments.objects.aggregate(total_revenue=Sum('payment_ammount'))
    total_revenue = total_revenue['total_revenue'] if total_revenue['total_revenue'] is not None else 0
    total_expense = Expense.objects.aggregate(total_expense=Sum('amount'))
    total_expense = total_expense['total_expense'] if total_expense['total_expense'] is not None else 0
    total_discount = Invoice.objects.aggregate(total_discount=Sum('discount_amount'))['total_discount'] or 0
    total_tax = Invoice.objects.aggregate(total_tax=Sum('tax_amount'))['total_tax'] or 0
    total_other_fees = Invoice.objects.aggregate(total_other_fees=Sum('other_fees_amount'))['total_other_fees'] or 0
    
    gross_profit = total_revenue-total_expense
    net_profit = gross_profit-(total_discount+total_tax+total_other_fees)
    
    context = {
        'title' : f'Profit & Loss Report',
        'gross_profit' : gross_profit,
        'net_profit' : net_profit,
        'total_revenue' : total_revenue,
        'total_expense' : total_expense,
        'total_discount' : total_discount,
        'total_tax' : total_tax,
        'total_other_fees' : total_other_fees,
        'current_year_total_payment' : current_year_total_payment,
        'current_month_total_payment' : current_month_total_payment,
        'previous_year_total_payment' : previous_year_total_payment
    }
    return render(request, 'crm/main/reports/partials/AllTimePF/profit_loss_print.html', context)
    
# Profit & Loss report
@login_required(login_url='signIn')
@admin_manager_role_required
def profitLossReport(request):
    current_year = timezone.now().year
    current_month = timezone.now().month
    previous_year = current_year - 1

    # Payments/Revenue Times
    payments_for_current_month = Payments.objects.filter(payment_date__year=current_year, payment_date__month=current_month)
    current_month_total_payment = payments_for_current_month.aggregate(Sum('payment_ammount'))['payment_ammount__sum'] or 0

    payments_for_previous_year = Payments.objects.filter(payment_date__year=previous_year)
    previous_year_total_payment = payments_for_previous_year.aggregate(Sum('payment_ammount'))['payment_ammount__sum'] or 0

    payments_for_current_year = Payments.objects.filter(payment_date__year=current_year)
    current_year_total_payment = payments_for_current_year.aggregate(Sum('payment_ammount'))['payment_ammount__sum'] or 0
    
    # Expense Times
    expenses_for_current_year = Expense.objects.filter(date_of_expense__year=current_year)
    current_year_total_expense = expenses_for_current_year.aggregate(Sum('amount'))['amount__sum'] or 0

    expenses_for_current_month = Expense.objects.filter(date_of_expense__year=current_year, date_of_expense__month=current_month)
    current_month_total_expense = expenses_for_current_month.aggregate(Sum('amount'))['amount__sum'] or 0

    expenses_for_previous_year = Expense.objects.filter(date_of_expense__year=previous_year)
    previous_year_total_expense = expenses_for_previous_year.aggregate(Sum('amount'))['amount__sum'] or 0
    
     # Calculate the total discount_amount, tax_amount, and other_fees_amount for the current year
    invoices_for_current_year = Invoice.objects.filter(billDate__year=current_year)
    current_year_total_discount = invoices_for_current_year.aggregate(Sum('discount_amount'))['discount_amount__sum'] or 0
    current_year_total_tax = invoices_for_current_year.aggregate(Sum('tax_amount'))['tax_amount__sum'] or 0
    current_year_total_other_fees = invoices_for_current_year.aggregate(Sum('other_fees_amount'))['other_fees_amount__sum'] or 0

    # Calculate the total discount_amount, tax_amount, and other_fees_amount for the current month
    invoices_for_current_month = Invoice.objects.filter(billDate__year=current_year, billDate__month=current_month)
    current_month_total_discount = invoices_for_current_month.aggregate(Sum('discount_amount'))['discount_amount__sum'] or 0
    current_month_total_tax = invoices_for_current_month.aggregate(Sum('tax_amount'))['tax_amount__sum'] or 0
    current_month_total_other_fees = invoices_for_current_month.aggregate(Sum('other_fees_amount'))['other_fees_amount__sum'] or 0

    # Calculate the total discount_amount, tax_amount, and other_fees_amount for the previous year
    invoices_for_previous_year = Invoice.objects.filter(billDate__year=previous_year)
    previous_year_total_discount = invoices_for_previous_year.aggregate(Sum('discount_amount'))['discount_amount__sum'] or 0
    previous_year_total_tax = invoices_for_previous_year.aggregate(Sum('tax_amount'))['tax_amount__sum'] or 0
    previous_year_total_other_fees = invoices_for_previous_year.aggregate(Sum('other_fees_amount'))['other_fees_amount__sum'] or 0
    
    
    # All time
    total_revenue = Payments.objects.aggregate(total_revenue=Sum('payment_ammount'))
    total_revenue = total_revenue['total_revenue'] if total_revenue['total_revenue'] is not None else 0
    total_expense = Expense.objects.aggregate(total_expense=Sum('amount'))
    total_expense = total_expense['total_expense'] if total_expense['total_expense'] is not None else 0
    total_discount = Invoice.objects.aggregate(total_discount=Sum('discount_amount'))['total_discount'] or 0
    total_tax = Invoice.objects.aggregate(total_tax=Sum('tax_amount'))['total_tax'] or 0
    total_other_fees = Invoice.objects.aggregate(total_other_fees=Sum('other_fees_amount'))['total_other_fees'] or 0

    gross_profit = total_revenue-total_expense
    net_profit = gross_profit-(total_discount+total_tax+total_other_fees)
    
    # This year calculation
    gross_profit_this_year = current_year_total_payment-current_year_total_expense
    net_profit_this_year = gross_profit_this_year-(current_year_total_discount+current_year_total_tax+current_year_total_other_fees)
    
    # This month calculation
    gross_profit_this_month = current_month_total_payment-current_month_total_expense
    net_profit_this_month = gross_profit_this_month-(current_month_total_discount+current_month_total_tax+current_month_total_other_fees)
    
    # previous year calculation
    gross_profit_previous_year = previous_year_total_payment-previous_year_total_expense
    net_profit_previous_year = gross_profit_previous_year-(previous_year_total_discount+previous_year_total_tax+previous_year_total_other_fees)

    context = {
        'title' : 'Profit/Loss Report',
        'current_year': current_year_total_payment,
        'current_month': current_month_total_payment,
        'previous_year': previous_year_total_payment,
        
        'total_revenue': total_revenue,
        'total_expense': total_expense,
        'total_discount': total_discount,
        'total_tax': total_tax,
        'total_other_fees': total_other_fees,
        
        'gross_profit': gross_profit,
        'net_profit': net_profit,
        
        'current_year_expense': current_year_total_expense,
        'current_month_expense': current_month_total_expense,
        'previous_year_expense': previous_year_total_expense,
        
        'current_year_discount_amount': current_year_total_discount,
        'current_year_tax_amount': current_year_total_tax,
        'current_year_other_fees_amount': current_year_total_other_fees,
        
        'current_month_discount_amount': current_month_total_discount,
        'current_month_tax_amount': current_month_total_tax,
        'current_month_other_fees_amount': current_month_total_other_fees,
        
        'previous_year_discount_amount': previous_year_total_discount,
        'previous_year_tax_amount': previous_year_total_tax,
        'previous_year_other_fees_amount': previous_year_total_other_fees,
        
        'gross_profit_this_year': gross_profit_this_year,
        'net_profit_this_year': net_profit_this_year,
        
        'gross_profit_this_month': gross_profit_this_month,
        'net_profit_this_month': net_profit_this_month,
        
        'gross_profit_previous_year': gross_profit_previous_year,
        'net_profit_previous_year': net_profit_previous_year,
    }

    return render(request, 'crm/main/reports/profit-loss.html', context)

# Payments report
@login_required(login_url='signIn')
@admin_manager_role_required
def paymentsReport(request):
    current_year = timezone.now().year
    current_month = timezone.now().month
    previous_year = current_year - 1
    
    # Payments/Revenue Times
    payments_for_current_month = Payments.objects.filter(payment_date__year=current_year, payment_date__month=current_month)
    current_month_total_payment = payments_for_current_month.aggregate(Sum('payment_ammount'))['payment_ammount__sum'] or 0

    payments_for_previous_year = Payments.objects.filter(payment_date__year=previous_year)
    previous_year_total_payment = payments_for_previous_year.aggregate(Sum('payment_ammount'))['payment_ammount__sum'] or 0

    payments_for_current_year = Payments.objects.filter(payment_date__year=current_year)
    current_year_total_payment = payments_for_current_year.aggregate(Sum('payment_ammount'))['payment_ammount__sum'] or 0
    
    # All time
    total_payments = Payments.objects.aggregate(total_revenue=Sum('payment_ammount'))
    total_payments = total_payments['total_revenue'] if total_payments['total_revenue'] is not None else 0
    all_payments = Payments.objects.all()
    
    # Payments Table filter
    # Filter payments for the current year
    payments_this_year = Payments.objects.filter(payment_date__year=current_year)

    # Filter payments for the current month
    payments_this_month = Payments.objects.filter(payment_date__year=current_year, payment_date__month=current_month)

    # Filter payments for the previous year
    payments_previous_year = Payments.objects.filter(payment_date__year=previous_year)

    
    context = {
        'title' : 'Payments report',
        'current_month_total_payment' : current_month_total_payment,
        'previous_year_total_payment' : previous_year_total_payment,
        'current_year_total_payment' : current_year_total_payment,
        'total_payments' : total_payments,
        'payments_this_year': payments_this_year,
        'payments_this_month': payments_this_month,
        'payments_previous_year': payments_previous_year,
        'all_payments' : all_payments,
        'current_year' : current_year,
        'current_month' : current_month,
        'previous_year' : previous_year,
    }
    
    return render(request, 'crm/main/reports/payments.html', context)

# Expense report
@login_required(login_url='signIn')
@admin_manager_role_required
def expenseReport(request):
    current_year = timezone.now().year
    current_month = timezone.now().month
    previous_year = current_year - 1
    
    # Expense Times
    expenses_for_current_year = Expense.objects.filter(date_of_expense__year=current_year)
    current_year_total_expense = expenses_for_current_year.aggregate(Sum('amount'))['amount__sum'] or 0

    expenses_for_current_month = Expense.objects.filter(date_of_expense__year=current_year, date_of_expense__month=current_month)
    current_month_total_expense = expenses_for_current_month.aggregate(Sum('amount'))['amount__sum'] or 0

    expenses_for_previous_year = Expense.objects.filter(date_of_expense__year=previous_year)
    previous_year_total_expense = expenses_for_previous_year.aggregate(Sum('amount'))['amount__sum'] or 0
    
    # Filter expenses for the current year
    expenses_this_year = Expense.objects.filter(date_of_expense__year=current_year)

    # Filter expenses for the current month
    expenses_this_month = Expense.objects.filter(date_of_expense__year=current_year, date_of_expense__month=current_month)

    # Filter expenses for the previous year
    expenses_previous_year = Expense.objects.filter(date_of_expense__year=previous_year)
    
    # All time
    total_expense = Expense.objects.aggregate(total_expense=Sum('amount'))
    total_expense = total_expense['total_expense'] if total_expense['total_expense'] is not None else 0
    all_time_expenses = Expense.objects.all()
    
    context = {
        'title' : 'Expense report',
        'current_month_total_expense' : current_month_total_expense,
        'previous_year_total_expense' : previous_year_total_expense,
        'current_year_total_expense' : current_year_total_expense,
        'expenses_this_year': expenses_this_year,
        'expenses_this_month': expenses_this_month,
        'expenses_previous_year': expenses_previous_year,
        'total_expense' : total_expense,
        'all_time_expenses_table' : all_time_expenses,
        'current_year' : current_year,
        'current_month' : current_month,
        'previous_year' : previous_year,
    }
    
    return render(request, 'crm/main/reports/expenses.html', context)

# Clients report
@login_required(login_url='signIn')
@admin_manager_role_required
def clientsReport(request):
    current_year = timezone.now().year
    current_month = timezone.now().month
    previous_year = current_year - 1
    
    # Filter clients for the current year
    clients_this_year = Guser.objects.filter(created__year=current_year)  
    
    # Filter clients for the current month
    clients_this_month = Guser.objects.filter(created__year=current_year, created__month=current_month)
    
    # Filter clients for the previous year
    clients_previous_year = Guser.objects.filter(created__year=previous_year)
    
    client_count_this_year = clients_this_year.count()
    client_count_this_month = clients_this_month.count() 
    client_count_previous_year = clients_previous_year.count()
    
    # All clients
    all_clients = Guser.objects.all()
    
    context = {
        'title' : 'Clients report',
        'clients_this_year': clients_this_year,
        'clients_this_month': clients_this_month,
        'clients_previous_year': clients_previous_year,
        'all_clients' : all_clients,
        'client_count_this_year' : client_count_this_year,
        'client_count_this_month' : client_count_this_month,
        'client_count_previous_year' : client_count_previous_year, 
        'current_year' : current_year,
        'current_month' : current_month,
        'previous_year' : previous_year,
    }
    
    return render(request, 'crm/main/reports/clients.html', context)

# CRM Invoice This Year Print
@login_required(login_url='signIn')
@admin_manager_role_required
def invoicePrintThisYear(request):
    current_year = timezone.now().year
    current_month = timezone.now().month
    previous_year = current_year - 1
    
    # Filter invoices for the current year
    invoices_this_year = Invoice.objects.filter(billDate__year=current_year)

    # Filter invoices for the current month
    invoices_this_month = Invoice.objects.filter(billDate__year=current_year, billDate__month=current_month)

    # Filter invoices for the previous year
    invoices_previous_year = Invoice.objects.filter(billDate__year=previous_year)

    # Get the counts of invoices in different statuses
    total_invoices_this_year = invoices_this_year.count()
    total_paid_this_year = invoices_this_year.filter(status='PAID').count()
    total_unpaid_this_year = invoices_this_year.filter(status='UNPAID').count()
    total_overdue_this_year = invoices_this_year.filter(status='OVERDUE').count()
    
    total_invoices_this_month = invoices_this_month.count()
    total_invoices_previous_year = invoices_previous_year.count()
    
    context = {
        'title' : f'{current_year} Invoice Report',
        
        'current_year': current_year,
        'current_month': current_month,
        'previous_year': previous_year,
        
        'invoices_this_year': invoices_this_year,
        'invoices_this_month': invoices_this_month,
        'invoices_previous_year': invoices_previous_year,
        
        'total_invoices_this_year': total_invoices_this_year,
        'total_paid_this_year': total_paid_this_year,
        'total_unpaid_this_year': total_unpaid_this_year,
        'total_overdue_this_year': total_overdue_this_year,
        'total_invoices_this_month' : total_invoices_this_month,
        'total_invoices_previous_year' : total_invoices_previous_year,
        
    }
    return render(request, 'crm/main/reports/partials/ThisYearINV/report.html', context)

# CRM Invoice This Month Print
@login_required(login_url='signIn')
@admin_manager_role_required
def invoicePrintThisMonth(request):
    current_year = timezone.now().year
    current_month = timezone.now().month
    previous_year = current_year - 1
    
    # Filter invoices for the current year
    invoices_this_year = Invoice.objects.filter(billDate__year=current_year)

    # Filter invoices for the current month
    invoices_this_month = Invoice.objects.filter(billDate__year=current_year, billDate__month=current_month)

    # Filter invoices for the previous year
    invoices_previous_year = Invoice.objects.filter(billDate__year=previous_year)
    
    total_invoices_this_month = invoices_this_month.count()
    total_paid_this_month = invoices_this_month.filter(status='PAID').count()
    total_unpaid_this_month = invoices_this_month.filter(status='UNPAID').count()
    total_overdue_this_month = invoices_this_month.filter(status='OVERDUE').count()

    total_invoices_this_year = invoices_this_year.count()
    total_invoices_previous_year = invoices_previous_year.count()
    
    context = {
        'title' : f'{current_month}/{current_year} Invoice Report',
        
        'current_year': current_year,
        'current_month': current_month,
        'previous_year': previous_year,
        
        'invoices_this_year': invoices_this_year,
        'invoices_this_month': invoices_this_month,
        'invoices_previous_year': invoices_previous_year,
        
        'total_invoices_this_month' : total_invoices_this_month,
        'total_paid_this_month' : total_paid_this_month,
        'total_unpaid_this_month' : total_unpaid_this_month,
        'total_overdue_this_month' : total_overdue_this_month,
        'total_invoices_this_year' : total_invoices_this_year,
        'total_invoices_previous_year' : total_invoices_previous_year
    }
    return render(request, 'crm/main/reports/partials/ThisMonthINV/report.html', context)

# CRM Invoice Previous Year Print
@login_required(login_url='signIn')
@admin_manager_role_required
def invoicePrintPrevYear(request):
    current_year = timezone.now().year
    current_month = timezone.now().month
    previous_year = current_year - 1
    
    # Filter invoices for the current year
    invoices_this_year = Invoice.objects.filter(billDate__year=current_year)

    # Filter invoices for the current month
    invoices_this_month = Invoice.objects.filter(billDate__year=current_year, billDate__month=current_month)

    # Filter invoices for the previous year
    invoices_previous_year = Invoice.objects.filter(billDate__year=previous_year)
    
    # Previous Year
    total_invoices_previous_year = invoices_previous_year.count()
    total_paid_previous_year = invoices_previous_year.filter(status='PAID').count()
    total_unpaid_previous_year = invoices_previous_year.filter(status='UNPAID').count()
    total_overdue_previous_year = invoices_previous_year.filter(status='OVERDUE').count()
    
    total_invoices_this_year = invoices_this_year.count()
    total_invoices_this_month = invoices_this_month.count()
    
    context = {
        'title' : f'{previous_year} Invoice Report',
        
        'current_year': current_year,
        'current_month': current_month,
        'previous_year': previous_year,
        
        'invoices_this_year': invoices_this_year,
        'invoices_this_month': invoices_this_month,
        'invoices_previous_year': invoices_previous_year,
        
        'total_invoices_previous_year' : total_invoices_previous_year,
        'total_paid_previous_year' : total_paid_previous_year,
        'total_unpaid_previous_year' : total_unpaid_previous_year,
        'total_overdue_previous_year' : total_overdue_previous_year,
        'total_invoices_this_year' : total_invoices_this_year,
        'total_invoices_this_month' : total_invoices_this_month
    }
    
    return render(request, 'crm/main/reports/partials/PrevYearINV/report.html', context)

# CRM Invoice All Time Print
@login_required(login_url='signIn')
@admin_manager_role_required
def invoicePrintAllTime(request):
    current_year = timezone.now().year
    current_month = timezone.now().month
    previous_year = current_year - 1
    
    # Filter invoices for the current year
    invoices_this_year = Invoice.objects.filter(billDate__year=current_year)

    # Filter invoices for the current month
    invoices_this_month = Invoice.objects.filter(billDate__year=current_year, billDate__month=current_month)

    # Filter invoices for the previous year
    invoices_previous_year = Invoice.objects.filter(billDate__year=previous_year)
    
    total_invoices_this_year = invoices_this_year.count()
    total_invoices_this_month = invoices_this_month.count()
    total_invoices_previous_year = invoices_previous_year.count()
    
    # All Time
    total_invoices = Invoice.objects.all().count()
    total_paid_invoices = Invoice.objects.filter(status="PAID").count()
    total_unpaid_invoices = Invoice.objects.filter(status="UNPAID").count()
    total_overdue_invoices = Invoice.objects.filter(status="OVERDUE").count()
    
    context = {
        'title' : 'Invoice Report',
        
        'current_year': current_year,
        'current_month': current_month,
        'previous_year': previous_year,
        
        'invoices_this_year': invoices_this_year,
        'invoices_this_month': invoices_this_month,
        'invoices_previous_year': invoices_previous_year,
        
        'total_invoices' : total_invoices,
        'total_paid_invoices' : total_paid_invoices,
        'total_unpaid_invoices' : total_unpaid_invoices,
        'total_overdue_invoices' : total_overdue_invoices,
        
        'total_invoices_this_year' : total_invoices_this_year,
        'total_invoices_this_month' : total_invoices_this_month,
        'total_invoices_previous_year' : total_invoices_previous_year
        
    }
    return render(request, 'crm/main/reports/partials/AllTimeINV/report.html', context)
    
# CRM Invoice reports
@login_required(login_url='signIn')
@admin_manager_role_required
def invoiceReport(request):
    current_year = timezone.now().year
    current_month = timezone.now().month
    previous_year = current_year - 1

    # Filter invoices for the current year
    invoices_this_year = Invoice.objects.filter(billDate__year=current_year)

    # Filter invoices for the current month
    invoices_this_month = Invoice.objects.filter(billDate__year=current_year, billDate__month=current_month)

    # Filter invoices for the previous year
    invoices_previous_year = Invoice.objects.filter(billDate__year=previous_year)

    # This Year
    total_invoices_this_year = invoices_this_year.count()
    total_paid_this_year = invoices_this_year.filter(status='PAID').count()
    total_unpaid_this_year = invoices_this_year.filter(status='UNPAID').count()
    total_overdue_this_year = invoices_this_year.filter(status='OVERDUE').count()

    # This Month
    total_invoices_this_month = invoices_this_month.count()
    total_paid_this_month = invoices_this_month.filter(status='PAID').count()
    total_unpaid_this_month = invoices_this_month.filter(status='UNPAID').count()
    total_overdue_this_month = invoices_this_month.filter(status='OVERDUE').count()

    # Previous Year
    total_invoices_previous_year = invoices_previous_year.count()
    total_paid_previous_year = invoices_previous_year.filter(status='PAID').count()
    total_unpaid_previous_year = invoices_previous_year.filter(status='UNPAID').count()
    total_overdue_previous_year = invoices_previous_year.filter(status='OVERDUE').count()
    
    # All Time
    total_invoices = Invoice.objects.all()
    total_count = total_invoices.count()
    total_paid_invoices = Invoice.objects.filter(status="PAID").count()
    total_unpaid_invoices = Invoice.objects.filter(status="UNPAID").count()
    total_overdue_invoices = Invoice.objects.filter(status="OVERDUE").count()

    context = {
        'title': 'Invoice Report',
        
        'current_year': current_year,
        'current_month': current_month,
        'previous_year': previous_year,
        
        'total_invoices' : total_invoices,
        'total_count' : total_count,
        'total_paid_invoices' : total_paid_invoices,
        'total_unpaid_invoices' : total_unpaid_invoices,
        'total_overdue_invoices' : total_overdue_invoices,
        
        'invoices_this_year': invoices_this_year,
        'invoices_this_month': invoices_this_month,
        'invoices_previous_year': invoices_previous_year,
        
        'total_invoices_this_year': total_invoices_this_year,
        'total_paid_this_year': total_paid_this_year,
        'total_unpaid_this_year': total_unpaid_this_year,
        'total_overdue_this_year': total_overdue_this_year,
        
        'total_invoices_this_month': total_invoices_this_month,
        'total_paid_this_month': total_paid_this_month,
        'total_unpaid_this_month': total_unpaid_this_month,
        'total_overdue_this_month': total_overdue_this_month,
        
        'total_invoices_previous_year': total_invoices_previous_year,
        'total_paid_previous_year': total_paid_previous_year,
        'total_unpaid_previous_year': total_unpaid_previous_year,
        'total_overdue_previous_year': total_overdue_previous_year,
    }

    return render(request, 'crm/main/reports/invoice.html', context)

@login_required(login_url='signIn')
@admin_manager_role_required
# CRM Project reports
def projectReport(request):
    current_year = timezone.now().year
    current_month = timezone.now().month
    previous_year = current_year - 1

    # Filter projects for the current year
    projects_this_year = crmProjects.objects.filter(start_date__year=current_year)

    # Filter projects for the current month
    projects_this_month = crmProjects.objects.filter(start_date__year=current_year, start_date__month=current_month)

    # Filter projects for the previous year
    projects_previous_year = crmProjects.objects.filter(start_date__year=previous_year)
    
    # All time
    all_projects = crmProjects.objects.all().order_by('-start_date')

    context = {
        'title': 'Project Report',
        
        'projects_this_year': projects_this_year,
        'projects_this_month': projects_this_month,
        'projects_previous_year': projects_previous_year,
        'all_projects' : all_projects,
        
        'current_year': current_year,
        'current_month': current_month,
        'previous_year': previous_year,
    }

    return render(request, 'crm/main/reports/project.html', context)

# Order Report
@login_required(login_url='signIn')
@admin_manager_role_required
def adminOrderReport(request):
    current_year = timezone.now().year
    current_month = timezone.now().month
    previous_year = current_year - 1
    
    # All Time Orders
    orders = Order.objects.filter(is_ordered=True)
    total_value = orders.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    order_pending = Order.objects.filter(status='pending', is_ordered=True)
    order_confirmed = Order.objects.filter(status='confirmed', is_ordered=True)
    order_completed = Order.objects.filter(status='completed', is_ordered=True)
    order_canceled = Order.objects.filter(status='canceled', is_ordered=True)
    
    # Order this month
    order_this_month = Order.objects.filter(ordered_at__year=current_year, ordered_at__month=current_month, is_ordered=True)
    total_value_this_month = order_this_month.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    pending_order_this_month = Order.objects.filter(is_ordered=True, status='pending', ordered_at__year=current_year, ordered_at__month=current_month)
    confirmed_order_this_month = Order.objects.filter(is_ordered=True, status='confirmed', ordered_at__year=current_year, ordered_at__month=current_month)
    completed_order_this_month = Order.objects.filter(is_ordered=True, status='completed', ordered_at__year=current_year, ordered_at__month=current_month)
    canceled_order_this_month = Order.objects.filter(is_ordered=True, status='canceled', ordered_at__year=current_year, ordered_at__month=current_month)
    
    # Order this year
    order_this_year = Order.objects.filter(is_ordered=True, ordered_at__year=current_year)
    total_value_this_year = order_this_year.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    pending_order_this_year = Order.objects.filter(is_ordered=True, status='pending', ordered_at__year=current_year)
    confirmed_order_this_year = Order.objects.filter(is_ordered=True, status='confirmed', ordered_at__year=current_year)
    completed_order_this_year = Order.objects.filter(is_ordered=True, status='completed', ordered_at__year=current_year)
    canceled_order_this_year = Order.objects.filter(is_ordered=True, status='canceled', ordered_at__year=current_year)
    
    # Order previous year
    order_previous_year = Order.objects.filter(is_ordered=True, ordered_at__year=previous_year)
    total_value_previous_year = order_previous_year.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    pending_order_previous_year = Order.objects.filter(is_ordered=True, status='pending', ordered_at__year=previous_year)
    confirmed_order_previous_year = Order.objects.filter(is_ordered=True, status='confirmed', ordered_at__year=previous_year)
    completed_order_previous_year = Order.objects.filter(is_ordered=True, status='completed', ordered_at__year=previous_year)
    canceled_order_previous_year = Order.objects.filter(is_ordered=True, status='canceled', ordered_at__year=previous_year)

    context = {
        'title' : 'Order Reports',
        'current_year': current_year,
        'current_month': current_month,
        'previous_year': previous_year,
        
        'orders' : orders,
        'total_value':total_value,
        'order_pending' : order_pending,
        'order_confirmed' : order_confirmed,
        'order_completed' : order_completed,
        'order_canceled' : order_canceled,
        
        'order_this_month' : order_this_month,
        'total_value_this_month' : total_value_this_month,
        'pending_order_this_month' : pending_order_this_month,
        'confirmed_order_this_month' : confirmed_order_this_month,
        'completed_order_this_month' : completed_order_this_month,
        'canceled_order_this_month' : canceled_order_this_month,
        
        'order_this_year' : order_this_year,
        'total_value_this_year' : total_value_this_year,
        'pending_order_this_year' : pending_order_this_year,
        'confirmed_order_this_year' : confirmed_order_this_year,
        'completed_order_this_year' : completed_order_this_year,
        'canceled_order_this_year' : canceled_order_this_year,
        
        'order_previous_year' : order_previous_year,
        'total_value_previous_year' : total_value_previous_year,
        'pending_order_previous_year' : pending_order_previous_year,
        'confirmed_order_previous_year': confirmed_order_previous_year,
        'completed_order_previous_year' : completed_order_previous_year,
        'canceled_order_previous_year' : canceled_order_previous_year,
    }
    
    return render(request, 'crm/main/reports/orders.html', context)

# Print This Year Orders
@login_required(login_url='signIn')
@admin_manager_role_required
def printThisYearOrders(request):
    
    current_year = timezone.now().year
    current_month = timezone.now().month
    previous_year = current_year - 1
    
    # All Time Orders
    order_this_year = Order.objects.filter(is_ordered=True, ordered_at__year=current_year)
    total_value_this_year = order_this_year.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    pending_order_this_year = Order.objects.filter(is_ordered=True, status='pending', ordered_at__year=current_year)
    confirmed_order_this_year = Order.objects.filter(is_ordered=True, status='confirmed', ordered_at__year=current_year)
    completed_order_this_year = Order.objects.filter(is_ordered=True, status='completed', ordered_at__year=current_year)
    canceled_order_this_year = Order.objects.filter(is_ordered=True, status='canceled', ordered_at__year=current_year)
    
    order_this_month = Order.objects.filter(is_ordered=True, ordered_at__year=current_year, ordered_at__month=current_month)
    order_previous_year = Order.objects.filter(is_ordered=True, ordered_at__year=previous_year)
    
    context = {
        'title' : f'{current_year} Order Report',
        
        'order_this_year' : order_this_year,
        'total_value_this_year' : total_value_this_year,
        'pending_order_this_year' : pending_order_this_year,
        'confirmed_order_this_year' : confirmed_order_this_year,
        'completed_order_this_year' : completed_order_this_year,
        'canceled_order_this_year' : canceled_order_this_year,
        
        'order_this_month' : order_this_month,
        'order_previous_year' : order_previous_year,
    }
    
    return render(request, 'crm/main/reports/partials/OrderPrint/thisyear.html', context)

# Print This Month Orders
@login_required(login_url='signIn')
@admin_manager_role_required
def printThisMonthOrders(request):
    
    current_year = timezone.now().year
    current_month = timezone.now().month
    previous_year = current_year - 1
    
    # All Time Orders
    order_this_month = Order.objects.filter(is_ordered=True, ordered_at__year=current_year, ordered_at__month=current_month)
    total_value_this_month = order_this_month.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    pending_order_this_month = Order.objects.filter(is_ordered=True, status='pending', ordered_at__year=current_year, ordered_at__month=current_month)
    confirmed_order_this_month = Order.objects.filter(is_ordered=True, status='confirmed', ordered_at__year=current_year, ordered_at__month=current_month)
    completed_order_this_month = Order.objects.filter(is_ordered=True, status='completed', ordered_at__year=current_year, ordered_at__month=current_month)
    canceled_order_this_month = Order.objects.filter(is_ordered=True, status='canceled', ordered_at__year=current_year, ordered_at__month=current_month)
    
    order_this_year = Order.objects.filter(is_ordered=True, ordered_at__year=current_year)
    order_previous_year = Order.objects.filter(is_ordered=True, ordered_at__year=previous_year)
    
    context = {
        'title' : f'{current_month}/{current_year} Order Report',
        
        'order_this_month' : order_this_month,
        'total_value_this_month' : total_value_this_month,
        'pending_order_this_month' : pending_order_this_month,
        'confirmed_order_this_month' : confirmed_order_this_month,
        'completed_order_this_month' : completed_order_this_month,
        'canceled_order_this_month' : canceled_order_this_month,
        
        'order_this_year' : order_this_year,
        'order_previous_year' : order_previous_year,
    }
    
    return render(request, 'crm/main/reports/partials/OrderPrint/thismonth.html', context)

# Print Previous Year Orders
@login_required(login_url='signIn')
@admin_manager_role_required
def printPrevYearOrders(request):
    
    current_year = timezone.now().year
    current_month = timezone.now().month
    previous_year = current_year - 1
    
    # All Time Orders
    order_previous_year = Order.objects.filter(is_ordered=True, ordered_at__year=previous_year)
    total_value_previous_year = order_previous_year.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    pending_order_previous_year = Order.objects.filter(is_ordered=True, status='pending', ordered_at__year=previous_year)
    confirmed_order_previous_year = Order.objects.filter(is_ordered=True, status='confirmed', ordered_at__year=previous_year)
    completed_order_previous_year = Order.objects.filter(is_ordered=True, status='completed', ordered_at__year=previous_year)
    canceled_order_previous_year = Order.objects.filter(is_ordered=True, status='canceled', ordered_at__year=previous_year)
    
    order_this_month = Order.objects.filter(is_ordered=True, ordered_at__year=current_year, ordered_at__month=current_month)
    order_this_year = Order.objects.filter(is_ordered=True, ordered_at__year=current_year)
    
    
    context = {
        'title' : f'{previous_year} Order Report',
        
        'order_previous_year' : order_previous_year,
        'total_value_previous_year' : total_value_previous_year,
        'pending_order_previous_year' : pending_order_previous_year,
        'confirmed_order_previous_year': confirmed_order_previous_year,
        'completed_order_previous_year' : completed_order_previous_year,
        'canceled_order_previous_year' : canceled_order_previous_year,
        
        'order_this_month' : order_this_month,
        'order_this_year' : order_this_year,
        
    }
    
    return render(request, 'crm/main/reports/partials/OrderPrint/prevyear.html', context)

# Print All Time Orders
@login_required(login_url='signIn')
@admin_manager_role_required
def printAllTimeOrders(request):
    
    current_year = timezone.now().year
    current_month = timezone.now().month
    previous_year = current_year - 1
    
    # All Time Orders
    orders = Order.objects.filter(is_ordered=True)
    total_value = orders.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    order_pending = Order.objects.filter(is_ordered=True, status='pending')
    order_confirmed = Order.objects.filter(is_ordered=True, status='confirmed')
    order_completed = Order.objects.filter(is_ordered=True, status='completed')
    order_canceled = Order.objects.filter(is_ordered=True, status='canceled')
    
    order_this_month = Order.objects.filter(is_ordered=True, ordered_at__year=current_year, ordered_at__month=current_month)
    order_this_year = Order.objects.filter(is_ordered=True, ordered_at__year=current_year)
    order_previous_year = Order.objects.filter(is_ordered=True, ordered_at__year=previous_year)
    
    context = {
        'title' : 'Order Report',
        
        'orders' : orders,
        'total_value':total_value,
        'order_pending' : order_pending,
        'order_confirmed' : order_confirmed,
        'order_completed' : order_completed,
        'order_canceled' : order_canceled,
        
        'order_this_month' : order_this_month,
        'order_this_year' : order_this_year,
        'order_previous_year' : order_previous_year,
    }
    
    return render(request, 'crm/main/reports/partials/OrderPrint/alltime.html', context)
    

# Activity log report
@login_required(login_url='signIn')
@admin_manager_role_required
def activityLogReport(request):
    recent_actions = LogEntry.objects.all().order_by('-action_time')
    
    context = {
        'title' : 'Activity Logs',
        'recent_actions' : recent_actions,
    }

    return render(request, 'crm/main/reports/logs.html', context)

# User report
# User Invoice Report
@login_required(login_url='signIn')
def userInvoiceReport(request):
    current_year = timezone.now().year
    current_month = timezone.now().month
    previous_year = current_year - 1
    
    usr = request.user
    
    # Filter invoices for the current year
    invoices_this_year = Invoice.objects.filter(client=usr, billDate__year=current_year)

    # Filter invoices for the current month
    invoices_this_month = Invoice.objects.filter(client=usr, billDate__year=current_year, billDate__month=current_month)

    # Filter invoices for the previous year
    invoices_previous_year = Invoice.objects.filter(client=usr, billDate__year=previous_year)
    
    # This Year
    total_invoices_this_year = invoices_this_year.count()
    total_paid_this_year = invoices_this_year.filter(status='PAID').count()
    total_unpaid_this_year = invoices_this_year.filter(status='UNPAID').count()
    total_overdue_this_year = invoices_this_year.filter(status='OVERDUE').count()

    # This Month
    total_invoices_this_month = invoices_this_month.count()
    total_paid_this_month = invoices_this_month.filter(status='PAID').count()
    total_unpaid_this_month = invoices_this_month.filter(status='UNPAID').count()
    total_overdue_this_month = invoices_this_month.filter(status='OVERDUE').count()

    # Previous Year
    total_invoices_previous_year = invoices_previous_year.count()
    total_paid_previous_year = invoices_previous_year.filter(status='PAID').count()
    total_unpaid_previous_year = invoices_previous_year.filter(status='UNPAID').count()
    total_overdue_previous_year = invoices_previous_year.filter(status='OVERDUE').count()
    
    # All Time
    total_invoices = Invoice.objects.filter(client=usr)
    total_count = total_invoices.count()
    total_paid_invoices = Invoice.objects.filter(client=usr, status="PAID").count()
    total_unpaid_invoices = Invoice.objects.filter(client=usr, status="UNPAID").count()
    total_overdue_invoices = Invoice.objects.filter(client=usr, status="OVERDUE").count()
    
    context = {
        'title' : 'Invoice Report',
        
        'current_year': current_year,
        'current_month' : current_month,
        'previous_year' : previous_year,
        
        'invoices_this_year' : invoices_this_year,
        'invoices_this_month' : invoices_this_month,
        'invoices_previous_year' : invoices_previous_year,
        
        'total_invoices_this_year': total_invoices_this_year,
        'total_paid_this_year': total_paid_this_year,
        'total_unpaid_this_year': total_unpaid_this_year,
        'total_overdue_this_year': total_overdue_this_year,
        
        'total_invoices_this_month': total_invoices_this_month,
        'total_paid_this_month': total_paid_this_month,
        'total_unpaid_this_month': total_unpaid_this_month,
        'total_overdue_this_month': total_overdue_this_month,
        
        'total_invoices_previous_year': total_invoices_previous_year,
        'total_paid_previous_year': total_paid_previous_year,
        'total_unpaid_previous_year': total_unpaid_previous_year,
        'total_overdue_previous_year': total_overdue_previous_year,
        
        'total_invoices' : total_invoices,
        'total_count' : total_count,
        'total_paid_invoices' : total_paid_invoices,
        'total_unpaid_invoices' : total_unpaid_invoices,
        'total_overdue_invoices' : total_overdue_invoices,
    }
    
    return render(request, 'user/main/reports/invoice.html', context)

@login_required(login_url='signIn')
def userInvoicePrintThisYear(request):
    current_year = timezone.now().year
    current_month = timezone.now().month
    previous_year = current_year - 1
    
    # Filter invoices for the current year
    invoices_this_year = Invoice.objects.filter(client=request.user, billDate__year=current_year)

    # Filter invoices for the current month
    invoices_this_month = Invoice.objects.filter(client=request.user, billDate__year=current_year, billDate__month=current_month)

    # Filter invoices for the previous year
    invoices_previous_year = Invoice.objects.filter(client=request.user, billDate__year=previous_year)

    # Get the counts of invoices in different statuses
    total_invoices_this_year = invoices_this_year.count()
    total_paid_this_year = invoices_this_year.filter(status='PAID').count()
    total_unpaid_this_year = invoices_this_year.filter(status='UNPAID').count()
    total_overdue_this_year = invoices_this_year.filter(status='OVERDUE').count()
    
    total_invoices_this_month = invoices_this_month.count()
    total_invoices_previous_year = invoices_previous_year.count()
    
    context = {
        'title' : f'{current_year} Invoice Report',
        
        'current_year': current_year,
        'current_month': current_month,
        'previous_year': previous_year,
        
        'invoices_this_year': invoices_this_year,
        'invoices_this_month': invoices_this_month,
        'invoices_previous_year': invoices_previous_year,
        
        'total_invoices_this_year': total_invoices_this_year,
        'total_paid_this_year': total_paid_this_year,
        'total_unpaid_this_year': total_unpaid_this_year,
        'total_overdue_this_year': total_overdue_this_year,
        'total_invoices_this_month' : total_invoices_this_month,
        'total_invoices_previous_year' : total_invoices_previous_year,
        
    }
    return render(request, 'user/main/reports/partials/inv_this_year.html', context)

@login_required(login_url='signIn')
def userInvoicePrintThisMonth(request):
    current_year = timezone.now().year
    current_month = timezone.now().month
    previous_year = current_year - 1
    
    # Filter invoices for the current year
    invoices_this_year = Invoice.objects.filter(client=request.user, billDate__year=current_year)

    # Filter invoices for the current month
    invoices_this_month = Invoice.objects.filter(client=request.user, billDate__year=current_year, billDate__month=current_month)

    # Filter invoices for the previous year
    invoices_previous_year = Invoice.objects.filter(client=request.user, billDate__year=previous_year)
    
    total_invoices_this_month = invoices_this_month.count()
    total_paid_this_month = invoices_this_month.filter(status='PAID').count()
    total_unpaid_this_month = invoices_this_month.filter(status='UNPAID').count()
    total_overdue_this_month = invoices_this_month.filter(status='OVERDUE').count()

    total_invoices_this_year = invoices_this_year.count()
    total_invoices_previous_year = invoices_previous_year.count()
    
    context = {
        'title' : f'{current_month}/{current_year} Invoice Report',
        
        'current_year': current_year,
        'current_month': current_month,
        'previous_year': previous_year,
        
        'invoices_this_year': invoices_this_year,
        'invoices_this_month': invoices_this_month,
        'invoices_previous_year': invoices_previous_year,
        
        'total_invoices_this_month' : total_invoices_this_month,
        'total_paid_this_month' : total_paid_this_month,
        'total_unpaid_this_month' : total_unpaid_this_month,
        'total_overdue_this_month' : total_overdue_this_month,
        'total_invoices_this_year' : total_invoices_this_year,
        'total_invoices_previous_year' : total_invoices_previous_year
    }
    return render(request, 'user/main/reports/partials/inv_this_month.html', context)

@login_required(login_url='signIn')
def userInvoicePrintPrevYear(request):
    current_year = timezone.now().year
    current_month = timezone.now().month
    previous_year = current_year - 1
    
    # Filter invoices for the current year
    invoices_this_year = Invoice.objects.filter(client=request.user, billDate__year=current_year)

    # Filter invoices for the current month
    invoices_this_month = Invoice.objects.filter(client=request.user, billDate__year=current_year, billDate__month=current_month)

    # Filter invoices for the previous year
    invoices_previous_year = Invoice.objects.filter(client=request.user, billDate__year=previous_year)
    
    # Previous Year
    total_invoices_previous_year = invoices_previous_year.count()
    total_paid_previous_year = invoices_previous_year.filter(status='PAID').count()
    total_unpaid_previous_year = invoices_previous_year.filter(status='UNPAID').count()
    total_overdue_previous_year = invoices_previous_year.filter(status='OVERDUE').count()
    
    total_invoices_this_year = invoices_this_year.count()
    total_invoices_this_month = invoices_this_month.count()
    
    context = {
        'title' : f'{previous_year} Invoice Report',
        
        'current_year': current_year,
        'current_month': current_month,
        'previous_year': previous_year,
        
        'invoices_this_year': invoices_this_year,
        'invoices_this_month': invoices_this_month,
        'invoices_previous_year': invoices_previous_year,
        
        'total_invoices_previous_year' : total_invoices_previous_year,
        'total_paid_previous_year' : total_paid_previous_year,
        'total_unpaid_previous_year' : total_unpaid_previous_year,
        'total_overdue_previous_year' : total_overdue_previous_year,
        'total_invoices_this_year' : total_invoices_this_year,
        'total_invoices_this_month' : total_invoices_this_month
    }
    
    return render(request, 'user/main/reports/partials/inv_prev_year.html', context)

@login_required(login_url='signIn')
def userInvoicePrintAllTime(request):
    current_year = timezone.now().year
    current_month = timezone.now().month
    previous_year = current_year - 1
    
    # Filter invoices for the current year
    invoices_this_year = Invoice.objects.filter(client=request.user, billDate__year=current_year)

    # Filter invoices for the current month
    invoices_this_month = Invoice.objects.filter(client=request.user, billDate__year=current_year, billDate__month=current_month)

    # Filter invoices for the previous year
    invoices_previous_year = Invoice.objects.filter(client=request.user, billDate__year=previous_year)
    
    total_invoices_this_year = invoices_this_year.count()
    total_invoices_this_month = invoices_this_month.count()
    total_invoices_previous_year = invoices_previous_year.count()
    
    # All Time
    total_invoices = Invoice.objects.filter(client=request.user).count()
    total_paid_invoices = Invoice.objects.filter(client=request.user, status="PAID").count()
    total_unpaid_invoices = Invoice.objects.filter(client=request.user, status="UNPAID").count()
    total_overdue_invoices = Invoice.objects.filter(client=request.user, status="OVERDUE").count()
    
    context = {
        'title' : 'Invoice Report',
        
        'current_year': current_year,
        'current_month': current_month,
        'previous_year': previous_year,
        
        'invoices_this_year': invoices_this_year,
        'invoices_this_month': invoices_this_month,
        'invoices_previous_year': invoices_previous_year,
        
        'total_invoices' : total_invoices,
        'total_paid_invoices' : total_paid_invoices,
        'total_unpaid_invoices' : total_unpaid_invoices,
        'total_overdue_invoices' : total_overdue_invoices,
        
        'total_invoices_this_year' : total_invoices_this_year,
        'total_invoices_this_month' : total_invoices_this_month,
        'total_invoices_previous_year' : total_invoices_previous_year
        
    }
    return render(request, 'user/main/reports/partials/inv_all_time.html', context)

# User Projects Report
@login_required(login_url='signIn')
def userProjectReport(request):
    current_year = timezone.now().year
    current_month = timezone.now().month
    previous_year = current_year - 1

    # Filter projects for the current year
    projects_this_year = crmProjects.objects.filter(client=request.user, start_date__year=current_year)

    # Filter projects for the current month
    projects_this_month = crmProjects.objects.filter(client=request.user, start_date__year=current_year, start_date__month=current_month)

    # Filter projects for the previous year
    projects_previous_year = crmProjects.objects.filter(client=request.user, start_date__year=previous_year)
    
    # All time
    all_projects = crmProjects.objects.filter(client=request.user).order_by('-start_date')

    context = {
        'title': 'Project Report',
        
        'projects_this_year': projects_this_year,
        'projects_this_month': projects_this_month,
        'projects_previous_year': projects_previous_year,
        'all_projects' : all_projects,
        
        'current_year': current_year,
        'current_month': current_month,
        'previous_year': previous_year,
    }

    return render(request, 'user/main/reports/project.html', context)

# User Payment Report
@login_required(login_url='signIn')
def userPaymentsReport(request):
    current_year = timezone.now().year
    current_month = timezone.now().month
    previous_year = current_year - 1
    user = request.user
    
    invoice_list = Invoice.objects.filter(client=user)

    # Filter payments for the current year
    payments_this_year = Payments.objects.filter(invoice__in = invoice_list, payment_date__year=current_year)

    # Filter payments for the current month
    payments_this_month = Payments.objects.filter(invoice__in = invoice_list, payment_date__year=current_year, payment_date__month=current_month)

    # Filter payments for the previous year
    payments_previous_year = Payments.objects.filter(invoice__in = invoice_list, payment_date__year=previous_year)
    
    # Payments/Revenue Times
    payments_for_current_month = Payments.objects.filter(invoice__in = invoice_list, payment_date__year=current_year, payment_date__month=current_month)
    current_month_total_payment = payments_for_current_month.aggregate(Sum('payment_ammount'))['payment_ammount__sum'] or 0

    payments_for_previous_year = Payments.objects.filter(invoice__in = invoice_list, payment_date__year=previous_year)
    previous_year_total_payment = payments_for_previous_year.aggregate(Sum('payment_ammount'))['payment_ammount__sum'] or 0

    payments_for_current_year = Payments.objects.filter(invoice__in = invoice_list, payment_date__year=current_year)
    current_year_total_payment = payments_for_current_year.aggregate(Sum('payment_ammount'))['payment_ammount__sum'] or 0
    
    # All time
    related_payments = Payments.objects.filter(invoice__in=invoice_list)
    total_payments = related_payments.aggregate(total_revenue=Sum('payment_ammount'))
    total_payments = total_payments['total_revenue'] if total_payments['total_revenue'] is not None else 0
    all_payments = Payments.objects.filter(invoice__in=invoice_list)

    context = {
        'title' : 'Payments report',
        'current_month_total_payment' : current_month_total_payment,
        'previous_year_total_payment' : previous_year_total_payment,
        'current_year_total_payment' : current_year_total_payment,
        'total_payments' : total_payments,
        'payments_this_year': payments_this_year,
        'payments_this_month': payments_this_month,
        'payments_previous_year': payments_previous_year,
        'all_payments' : all_payments,
        'current_year' : current_year,
        'current_month' : current_month,
        'previous_year' : previous_year,
    }
    
    return render(request, 'user/main/reports/payment.html', context)



# Error Page
def error_404(request, exception):
    return render(request, 'error/error_404.html', status=404)