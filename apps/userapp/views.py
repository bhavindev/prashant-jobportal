from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib import messages
from apps.userapp.models import *
from apps.authapp.models import *
from apps.crm.models import *
from apps.userapp.forms import *
from apps.legals.models import agreement
from django.contrib.auth.decorators import login_required
from core.decorators import user_role_required
from django.db.models import F, Sum, Q
from apps.order.models import  *
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.html import strip_tags
from django.core.mail import send_mail
from apps.settings.models import *
from django.conf import settings
from django.contrib.auth import get_user_model
from apps.userapp.sslcommerze import sslCommerzGateway
from apps.userapp.paypal import invPaypalGeteway
from apps.userapp.instamojo import invMojoGetaway
from apps.userapp.stripe import invStripeGateway
from apps.userapp.paymob import paymobGateway


# User Home Dashboard
@login_required
def userDashboard(request):
    user = request.user

    # User Project
    projects = crmProjects.objects.filter(client=user).order_by('-start_date')

    # User Invoicing
    user_invoices = Invoice.objects.filter(client=user).order_by('-date_created')
    user_payments = Payments.objects.filter(invoice__client=user).order_by('-payment_date')
    total_invoiced = 0
    for invoice in user_invoices:
        total_product_price = invoice.sub_total
        total_product_price -= invoice.discount_amount
        total_product_price += invoice.tax_amount + invoice.other_fees_amount
        total_invoiced += total_product_price
    total_payments = Payments.objects.filter(invoice__client=user).aggregate(
        total=Sum('payment_ammount'))['total'] or 0

    # User Due
    total_due = total_invoiced - total_payments

    # Calculate the percentage paid by the user
    percentage_paid = (total_payments / total_invoiced) * 100 if total_invoiced != 0 else 0

    # Round the percentage to two decimal places
    percentage_paid = round(percentage_paid, 2)

    # Tickets
    tickets = supportTicket.objects.filter(client=user).order_by('-created_at')

    context = {
        'title': 'Dashboard',
        'invoices': user_invoices,
        'payments': user_payments,
        'projects': projects,
        'tickets': tickets,
        'total_invoiced': total_invoiced,
        'total_payments': total_payments,
        'total_due': total_due,
        'percentage_paid': percentage_paid,
    }
    return render(request, 'user/main/index.html', context)


# User Tickets
@login_required(login_url='signIn')
@user_role_required
def ticketList(request):
    tickets = supportTicket.objects.filter(client=request.user).order_by('-created_at')

    context = {
        'title': 'Tickets',
        'tickets': tickets,
    }
    return render(request, 'user/main/tickets/tickets.html', context)


@login_required(login_url='signIn')
@user_role_required
def userTicketCreate(request):
    if request.method == "POST":
        form = SupportTicketForm(request.POST, user=request.user)
        if form.is_valid():
            new_ticket = form.save(commit=False)
            new_ticket.client = request.user
            new_ticket.save()

            try:
                # Send email to all users with the 'Admin' role
                website_settings = websiteSetting.objects.first()
                footer = HeaderFooter.objects.first()
                subject = f'New Support Ticket: {new_ticket.title}'
                from_email = f'"{website_settings.name}" <{settings.EMAIL_HOST_USER}>'

                admin_users = get_user_model().objects.filter(role='Admin')

                if admin_users.exists():
                    recipient_list = [admin_user.email for admin_user in admin_users]
                    admin_view_link = request.build_absolute_uri(reverse('ticketView', args=[str(new_ticket.id)]))
                    html_message = render_to_string('user/main/email/admin_new_ticket_email.html', {
                        'user': 'Admin',
                        'client': new_ticket.client,
                        'ticket': new_ticket,
                        'footer': footer,
                        'admin_view_link': admin_view_link,
                    })
                    plain_message = strip_tags(html_message)

                    send_mail(subject, plain_message, from_email, recipient_list, html_message=html_message)
                    messages.success(request, 'Ticket created successfully!')
                else:
                    messages.warning(request, 'No users with the role "Admin" found. Email not sent.')

            except:
                messages.success(request, 'Ticket created successfully!')

            return redirect('userTickets')
    else:
        form = SupportTicketForm(user=request.user)

    context = {
        'title': 'Create Ticket',
        'form': form,
    }
    return render(request, 'user/main/tickets/create.html', context)


@login_required(login_url='signIn')
@user_role_required
def userTicketDelete(request, id):
    ticket_list = supportTicket.objects.filter(client=request.user)
    ticket = get_object_or_404(ticket_list, id=id)
    if ticket.client == request.user:
        ticket.delete()
        messages.success(request, 'Ticket deleted successfully!')
        return redirect('userTickets')
    else:
        return redirect('signIn')


@login_required(login_url='signIn')
@user_role_required
def userticketView(request, id):
    ticket = get_object_or_404(supportTicket, id=id)
    replyform = ReplyForm()

    context = {
        'title': 'View Ticket',
        'ticket': ticket,
        'replyform': replyform,
        'replies': ticket.replies.all()
    }
    if ticket.client == request.user:
        return render(request, 'user/main/tickets/view.html', context)
    else:
        return redirect('signIn')

# User Projects
@login_required(login_url='signIn')
@user_role_required
def userProjects(request):
    user = request.user
    projects = crmProjects.objects.filter(client=user).order_by('-start_date')

    context = {
        'title': 'Projects',
        'projects': projects,
    }
    return render(request, 'user/main/projects/projects.html', context)


@login_required(login_url='signIn')
@user_role_required
def projectDetail(request, slug):
    user = request.user
    # User Project Overview
    user_projects = crmProjects.objects.filter(client=user)
    project_single = get_object_or_404(user_projects, slug=slug)

    # User Payment Overview
    user_invoices = Invoice.objects.filter(project=project_single).order_by('-date_created')
    total_invoiced = 0
    for invoice in user_invoices:
        total_product_price = invoice.sub_total
        total_product_price -= invoice.discount_amount
        total_product_price += invoice.tax_amount + invoice.other_fees_amount
        total_invoiced += total_product_price
    total_payments = Payments.objects.filter(invoice__project=project_single).aggregate(
        total=Sum('payment_ammount'))['total'] or 0

    # User Due
    total_due = total_invoiced - total_payments

    # Check if either total_payments or total_invoiced is zero
    if total_payments == 0 or total_invoiced == 0:
        percentage_paid = 0
    else:
        percentage_paid = (total_payments / total_invoiced) * 100
        percentage_paid = round(percentage_paid, 2)

    # User Tasks for Particular Project
    tasks = crmTasks.objects.filter(project=project_single)

    # User Tickets For Particular Project
    tickets = supportTicket.objects.filter(client=request.user, project=project_single)

    # User Invoice for Particular Project
    invoices = Invoice.objects.filter(client=user, project=project_single)

    # User Payment for particular Project Invoice)
    payments = Payments.objects.filter(invoice__in=invoices)

    context = {
        'project': project_single,
        'percentage_paid': int(percentage_paid),
        'total_invoiced': total_invoiced,
        'total_payments': total_payments,
        'total_due': total_due,
        'tickets': tickets,
        'invoices': invoices,
        'payments': payments,
        'tasks': tasks,
    }
    return render(request, 'user/main/projects/view.html', context)


# User Invoices
@login_required(login_url='signIn')
@user_role_required
def userInvoices(request):
    user = request.user

    invoice_list = Invoice.objects.filter(client=user).order_by('-date_created')

    context = {
        'title': 'Invoices',
        'invoices': invoice_list,
    }
    return render(request, 'user/main/invoice/invoice.html', context)


@login_required(login_url='signIn')
@user_role_required
def viewUserPDFInvoice(request, slug):
    try:
        invoice = Invoice.objects.get(slug=slug)
    except:
        messages.error(request, 'Something went wrong')
        return redirect('invoices')
    
    try:
        payment = Payments.objects.get(invoice=invoice)
    except Payments.DoesNotExist:
        payment = None 
        
    payment_amount = payment.payment_ammount if payment else 0
        

    discount = invoice.discount_amount or 0
    tax = invoice.tax_amount or 0
    other_fee_name = invoice.other_fees_name
    other_fee_amount = invoice.other_fees_amount or 0
    total = (invoice.sub_total or 0) + tax + other_fee_amount - discount
    due = total - payment_amount
    
    protocol = 'https' if request.is_secure() else 'http'
    
    # Payment Processing
    if request.method == 'POST':
        if 'sslcommerze' in request.POST:
            print(invoice.slug)
            response = sslCommerzGateway(name=invoice.client.userprofile.name, email=invoice.client.email, price=due, phone=invoice.client.userprofile.phone, address=invoice.client.userprofile.address, city=invoice.client.userprofile.city, country=invoice.client.userprofile.country, client=invoice.client.pk, host=request.get_host(), protocol=protocol, slug=invoice.slug)
            if response['status'] == 'SUCCESS':
                redirect_url = response['GatewayPageURL']
                return redirect(redirect_url)
            else:
                print(response)
                return redirect('view_cart')
            
        elif 'paypal' in request.POST:
            paypal_url = invPaypalGeteway(price=due, host=request.get_host(), protocol=protocol, slug=invoice.slug)
            return redirect(paypal_url)
        
        elif 'instamojo' in request.POST:
            mojo_url = invMojoGetaway(request, price=due, email=invoice.client.email, protocol=protocol, host=request.get_host(), slug=invoice.slug)
            if mojo_url is not None:
                return redirect(mojo_url)
            else:
                print("Error: Instamojo payment processing failed.")
                return redirect('viewUserPDFInvoice', slug=invoice.slug)
        
        elif 'stripe' in request.POST:
            gateway_url = invStripeGateway(host=request.get_host(), protocol=protocol, price=due, slug=invoice.slug)
            return redirect(gateway_url)
        
        elif 'paymob' in request.POST:
            try:
                price = due
                name_parts = invoice.client.userprofile.name.split()
                if len(name_parts) > 1:
                    first_name = name_parts[0]
                    last_name = " ".join(name_parts[1:])
                else:
                    first_name = name_parts[0]
                    last_name = ""  
                    
                billing_data = {
                    "apartment": invoice.client.userprofile.address,
                    "email": invoice.client.email,
                    "floor": "",
                    "first_name": first_name,
                    "last_name": last_name,
                    "street": invoice.client.userprofile.address,
                    "building": "",
                    "phone_number": invoice.client.userprofile.phone,
                    "shipping_method": "",
                    "postal_code": invoice.client.userprofile.zipcode,
                    "city": invoice.client.userprofile.city,
                    "country": invoice.client.userprofile.country
                }
                items_data = [
                    {
                        "name": f'Payment for Invoice #{invoice.number}',
                        "amount": price * 100,
                        "description": "",
                        "quantity": 1
                    }
                ]

                payment_url = paymobGateway(user=request.user, host=request.get_host(), protocol=protocol, price=price, billing_data=billing_data, items=items_data, slug=invoice.slug)
                return redirect(payment_url)
            except Exception as e:
                print(f"Failed to create payment intention. Error: {e}")
                return redirect('viewUserPDFInvoice', slug=invoice.slug)
            

    context = {
        'invoice': invoice,
        'discount': discount,
        'tax': tax,
        'other_fee_name': other_fee_name,
        'other_fee_amount': other_fee_amount,
        'total': total,
        'payment_amount' : payment_amount,
        'due' : due
    }
    
    if invoice.client == request.user:
        return render(request, 'user/main/invoice/partials/inv.html', context)
    else:
        return redirect('signIn')

# Invoice payment confirmation
@login_required(login_url='signIn')
def inv_payment_confirmation(request, slug):
    invoice = get_object_or_404(Invoice, slug=slug)
    payment = get_object_or_404(Payments, invoice=invoice)
    paid_amount = request.GET.get('paid_amount')

    first_visit = request.GET.get('first_visit', None)

    if first_visit:
        invoice_items = InvoiceItem.objects.filter(invoice=invoice)
        return render(request, 'user/main/invoice/partials/inv_confirm.html', {'invoice': invoice, 'invoice_items': invoice_items, 'payment': payment, 'paid_amount': paid_amount})

    return redirect('userInvoices')


@login_required(login_url='signIn')
def inv_payment_failed(request):
    return render(request, 'user/main/ecom/payment-fail.html')

# User Payments
@login_required(login_url='signIn')
@user_role_required
def userPayments(request):
    user = request.user
    invoice_list = Invoice.objects.filter(client=user)
    payments = Payments.objects.filter(invoice__in=invoice_list).order_by('-payment_date')

    context = {
        'title': 'Payments',
        'payments': payments,
    }
    return render(request, 'user/main/payments/payments.html', context)


# User Profile
@login_required(login_url='signIn')
@user_role_required
def customUserProfile(request):
    user = request.user

    # Overview
    user_project = crmProjects.objects.filter(client=user)
    invoices = Invoice.objects.filter(client=user)
    tickets = supportTicket.objects.filter(client=user)

    # User Project Pagination
    paginator = Paginator(user_project, 10)
    page_number = request.GET.get('page')
    projects = paginator.get_page(page_number)

    # Password Change
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your password has been changed.')
            return redirect('customUserProfile') 
    else:
        form = CustomPasswordChangeForm(request.user)
        print(form.errors)

    context = {
        'title': 'Profile',
        'projects_count': user_project,
        'projects': projects,
        'invoices': invoices,
        'tickets': tickets,
        'form': form
    }
    return render(request, 'user/main/profile/profile.html', context)


@login_required(login_url='signIn')
@user_role_required
def profile_edit_view(request):
    user_profile = request.user.userprofile
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('customUserProfile') 
    else:
        form = UserProfileForm(instance=user_profile)

    context = {
        'title': 'Edit Profile',
        'form': form,
        'profile': user_profile,
    }
    return render(request, 'user/main/profile/edit.html', context)


# User Agreements
@login_required(login_url='signIn')
@user_role_required
def userAgreements(request):
    user = request.user
    user_agreement = agreement.objects.filter(client=user).order_by('-singed_at')
    context = {
        'title': 'Agreements',
        'user_agreement': user_agreement,
    }
    return render(request, 'user/main/agreement/agreements.html', context)


@login_required(login_url='signIn')
@user_role_required
def userAgreementDetail(request, id):
    user = request.user
    user_agreement = agreement.objects.filter(client=user)

    agreement_data = get_object_or_404(user_agreement, id=id)
    context = {
        'data': agreement_data
    }
    return render(request, 'user/main/agreement/detail.html', context)

# User Orders
@login_required(login_url='signIn')
@user_role_required
def userOrders(request):
    user = request.user
    orders = Order.objects.filter(user=user, is_ordered=True).order_by('-ordered_at')
    pending_orders = Order.objects.filter(user=user, status='pending', is_ordered=True).count()
    confirmed_orders = Order.objects.filter(user=user, status='confirmed', is_ordered=True).count()
    canceled_orders = Order.objects.filter(user=user, status='canceled', is_ordered=True).count()
    
    context = {
        'title': 'Orders',
        'orders': orders,
        'pending_orders': pending_orders,
        'confirmed_orders': confirmed_orders,
        'canceled_orders': canceled_orders,
    }
    return render(request, 'user/main/orders/orders.html', context)

def error_404(request, exception):
    return render(request, 'error/error_404.html', status=404)

# User Order Details
@login_required(login_url='signIn')
@user_role_required
def userOrderDetail(request, order_id):
    order = get_object_or_404(Order, order_id=order_id, is_ordered=True, user=request.user)
    cart_items = Cart.objects.filter(order=order)
    
    context = {
        'order' : order,
        'cart_items' : cart_items,
    }
    
    return render(request, 'user/main/orders/order-detail.html', context)
