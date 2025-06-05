import stripe
from apps.settings.models import paymentMethod, websiteSetting
from django.shortcuts import redirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from apps.order.models import *
from django.contrib import messages
from django.urls import reverse
from apps.crm.models import Payments, Invoice
from datetime import date

def invStripeGateway(host, protocol, price, slug):
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
        success_url=f'{protocol}://{host}/invoice/stripe/success?session_id={{CHECKOUT_SESSION_ID}}&price={price}&inv_slug={slug}',
        mode='payment',
    )
 
    # Redirect the user to Stripe Checkout
    return checkout_session.url

@csrf_exempt
def inv_stripe_success(request):
    session_id = request.GET.get('session_id')
    session = stripe.checkout.Session.retrieve(session_id)
    slug = request.GET.get('inv_slug')
    invoice = get_object_or_404(Invoice, slug=slug)
    paid_amount = request.GET.get('price')
    
    if session:
        invoice.status = "PAID"
        invoice.save()
        # Checkig existing payment or Creating a payment for the invoice
        if Payments.objects.filter(invoice=invoice).exists():
            payment = Payments.objects.get(invoice=invoice)
            if paid_amount is not None:
                payment.payment_ammount += float(paid_amount)
            payment.transaction_id = session_id,
            payment.payment_method = 'Stripe'
            payment.payment_date = date.today()
            payment.payment_note = ""
            payment.save()
        else:
            payment = Payments.objects.create(
                invoice=invoice,
                title=invoice.number + " Payment",
                payment_method='Stripe',
                payment_ammount=paid_amount,
                transaction_id=session_id,
                payment_date=date.today(),
                payment_note="",
            )
        messages.success(request, 'Payment successful!')
        redirect_url = reverse('inv_payment_confirmation', args=[invoice.slug]) + '?first_visit=true&paid_amount=' + paid_amount
        return redirect(redirect_url)
    else:
      return redirect('viewUserPDFInvoice', slug=invoice.slug)