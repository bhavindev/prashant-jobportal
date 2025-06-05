from instamojo_wrapper import Instamojo
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect, render, get_object_or_404
from apps.order.models import *
from django.contrib import messages
from django.urls import reverse
from uuid import uuid4
from apps.crm.models import crmProjects, Payments, Invoice, InvoiceItem
from datetime import date
from apps.settings.models import websiteSetting, paymentMethod
from django.http import HttpResponse
import json


def invMojoGetaway(request, price, email, host, protocol, slug):
    credential = paymentMethod.objects.first()
    if credential.instamojo_is_sandbox:
        api = Instamojo(api_key=credential.instamojo_api_key, auth_token=credential.instamojo_auth_token, endpoint='https://test.instamojo.com/api/1.1/')
    else:
        api = Instamojo(api_key=credential.instamojo_api_key, auth_token=credential.instamojo_auth_token)

    try:
        response = api.payment_request_create(
            amount=str(price),
            purpose='Website Payment',
            send_email=True,
            email=str(email),
            redirect_url=f"{protocol}://{host}/invoice/instamojo/success?inv_slug={slug}&price={price}",
        )

        paymentID = response['payment_request']['id']

        request.session['instamojo_paymentID'] = paymentID

        return response['payment_request']['longurl']
    except KeyError as e:
        print(f"KeyError: {e}. Response from Instamojo: {response}")
        return None
    

@csrf_exempt
def inv_instamojo_success(request):
    paymentID = request.session.get('instamojo_paymentID')
    slug = request.GET.get('inv_slug')
    invoice = get_object_or_404(Invoice, slug=slug)
    paid_amount = request.GET.get('price')

    if paymentID:
        invoice.status = "PAID"
        invoice.save()
        # Checkig existing payment or Creating a payment for the invoice
        if Payments.objects.filter(invoice=invoice).exists():
            payment = Payments.objects.get(invoice=invoice)
            if paid_amount is not None:
                payment.payment_ammount += float(paid_amount)
            payment.transaction_id = paymentID,
            payment.payment_method = 'Instamojo'
            payment.payment_date = date.today()
            payment.payment_note = ""
            payment.save()
        else:
            payment = Payments.objects.create(
                invoice=invoice,
                title=invoice.number + " Payment",
                payment_method='Instamojo',
                payment_ammount=paid_amount,
                transaction_id=paymentID,
                payment_date=date.today(),
                payment_note="",
            )
        messages.success(request, 'Payment successful!')
        redirect_url = reverse('inv_payment_confirmation', args=[invoice.slug]) + '?first_visit=true&paid_amount=' + paid_amount
        return redirect(redirect_url)
    else:
        return redirect('viewUserPDFInvoice', slug=invoice.slug)

@csrf_exempt
def instamojo_failed(request):
    messages.warning(request, 'Payment failed!')
    return redirect('payment_failed')