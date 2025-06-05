import paypalrestsdk
from apps.settings.models import paymentMethod, websiteSetting
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect, render, get_object_or_404
from apps.order.models import *
from django.contrib import messages
from django.urls import reverse
from uuid import uuid4
from apps.crm.models import crmProjects, Payments, Invoice, InvoiceItem
from datetime import date


def invPaypalGeteway(price, host, protocol, slug):
    credential = paymentMethod.objects.first()
    web_settings = websiteSetting.objects.first()
    paypalrestsdk.configure({
        "mode": "sandbox" if credential.paypal_is_sandbox else "live",
        'client_id': credential.paypal_client_id,
        'client_secret': credential.paypal_client_secret})

    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"},
        "redirect_urls": {
            "return_url": f"{protocol}://{host}/invoice/paypal/success?inv_slug={slug}&price={price}",
            "cancel_url": f"{protocol}://{host}/invoice/paypal/failed"},
        "transactions": [{
            "amount": {
                "total": f"{price}",
                "currency": str(web_settings.currency_name)},
            "description": "",
            "inv_slug": slug,}]})
    print(payment)
    if payment.create():

        for link in payment.links:
            if link.rel == "approval_url":
                approval_url = str(link.href)

                return approval_url
    else:
        print(payment.errors)


@csrf_exempt
def inv_paypal_success(request):
    paymentID = request.GET.get('paymentId')
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
            payment.payment_method = 'PayPal'
            payment.payment_date = date.today()
            payment.payment_note = ""
            payment.save()
        else:
            payment = Payments.objects.create(
                invoice=invoice,
                title=invoice.number + " Payment",
                payment_method='PayPal',
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
def inv_paypal_failed(request):
    messages.warning(request, 'Payment failed!')
    return redirect('payment_failed')
