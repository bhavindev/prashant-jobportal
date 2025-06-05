import stripe
from apps.settings.models import paymentMethod, websiteSetting
from django.shortcuts import redirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from apps.order.models import *
from django.contrib import messages
from django.urls import reverse
from uuid import uuid4
from apps.crm.models import crmProjects, Payments, Invoice, InvoiceItem
from datetime import date

def stripeGateway(host, protocol, price):
    credential = paymentMethod.objects.first()
    web_settings = websiteSetting.objects.first()
    stripe.api_key = credential.stripe_secret_key
    unit_amount = int(price) * 100
    
    # Add the line items to the checkout session
    checkout_session = stripe.checkout.Session.create(
        currency=str(web_settings.currency_name.lower()),
        line_items=[
            {
                'price_data': {
                    'currency': str(web_settings.currency_name.lower()),
                    'unit_amount': unit_amount,
                    'product_data': {
                        'name': 'payment',
                    },
                },
                'quantity': 1,
            }
        ],
        success_url=f'{protocol}://{host}/order/stripe/success?session_id={{CHECKOUT_SESSION_ID}}',
        mode='payment',
    )
 
    # Redirect the user to Stripe Checkout
    return checkout_session.url

@csrf_exempt
def stripe_success(request):
    order_settings = websiteSetting.objects.first()
    number = 'INV-' + str(uuid4()).split('-')[1]
    session_id = request.GET.get('session_id')
    session = stripe.checkout.Session.retrieve(session_id)
    user = request.user
    order = get_object_or_404(Order, user=user, is_ordered=False)
    
    if session:
        order.payment_method = 'stripe'
        order.is_ordered = True
        order.status = "confirmed"
        order.transaction_id = session_id
        order.save()
        
        if order_settings.is_auto_invoice_enable:
                
            # Creating a project for the invoice
            project = crmProjects.objects.create(
                title=f"Project of Order {order.order_id}",
                start_date=date.today(),
                deadline=date.today(), 
                price=order.total_amount,
                client=order.user,
                label='started',
            )
                
            # Creating an invoice for the user
            invoice = Invoice.objects.create(
                number=number,
                client=order.user, 
                billDate=date.today(),
                dueDate=date.today(),
                project=project,
                title=f"Invoice for Order {order.order_id}",
                sub_total=order.total_amount,
                discount_amount=0,
                tax_amount=0, 
                other_fees_name="Other Fees", 
                other_fees_amount=0,
            )
            invoice.products.set(order.products.all())
            
            # Adding invoice items based on order products
            for cart_item in Cart.objects.filter(order=order):
                invoice_item = InvoiceItem.objects.create(
                    invoice=invoice,
                    item=cart_item.product,
                    unit_type=cart_item.unit_type,
                    quantity=cart_item.quantity,
                    unit_price=cart_item.unit_price,
                    sub_total=cart_item.subtotal,
                )

            invoice.sub_total = invoice.get_total()
            invoice.save()
                
            # Creating a payment for the invoice
            payment_method_mapping = {
            'stripe': 'Stripe',
            }
            readable_payment_method = payment_method_mapping.get(order.payment_method, order.payment_method)
            payment = Payments.objects.create(
                invoice=invoice,  
                title=f"Invoice #{number} Payment",
                transaction_id=session_id,
                payment_method=readable_payment_method, 
                payment_ammount=invoice.sub_total,
                payment_date=date.today(),
                payment_note="Your Payment Note", 
            )
            
        messages.success(request, 'Order placed successfully!')
        redirect_url = reverse('order_confirmation', args=[order.id]) + '?first_visit=true'
        return redirect(redirect_url)
    else:
      return redirect('checkout')