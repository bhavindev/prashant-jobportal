from sslcommerz_lib import SSLCOMMERZ
from apps.settings.models import *
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect, get_object_or_404
from apps.order.models import *
from django.contrib import messages
from django.urls import reverse
from apps.crm.models import Invoice, Payments
from uuid import uuid4
from datetime import date


def sslCommerzGateway(name, email, price, phone, address, city, country, client, host, protocol, slug):
    credential = paymentMethod.objects.first()
    web_settings = websiteSetting.objects.first()
    settings = {'store_id': credential.ssl_commerze_store_id, 'store_pass': credential.ssl_commerze_store_pass,
                'issandbox': credential.ssl_commerze_is_sandbox}
    sslcommez = SSLCOMMERZ(settings)

    post_body = {
        'total_amount': price,
        'currency': str(web_settings.currency_name),
        'tran_id': "12345",
        'cancel_url': f"{protocol}://{host}/invoice/sslcommerze/failed",
        'emi_option': 0,
        'cus_name': name,
        'cus_email': email,
        'cus_phone': phone,
        'cus_add1': address,
        'cus_city': city,
        'cus_country': country,
        'shipping_method': "NO",
        'multi_card_name': "",
        'num_of_item': 1,
        'product_name': "Test",
        'product_category': "Test Category",
        'product_profile': "general",
        "success_url": f"{protocol}://{host}/invoice/sslcommerze/success/",
        'fail_url': f"{protocol}://{host}/invoice/sslcommerze/failed/",
        "value_a": client,
        "value_b" : slug,
        "value_c": price,

    }

    response = sslcommez.createSession(post_body)

    return response


@csrf_exempt
def inv_sslc_success(request):
    if request.POST:
        val_id = request.POST.get('val_id')
        slug =  request.POST.get('value_b')
        paid_amount = request.POST.get('value_c')
        invoice = get_object_or_404(Invoice, slug=slug)
        print('Printed', invoice, val_id, paid_amount, slug)
        if val_id:
            invoice.status = "PAID"
            invoice.save()

            # Checkig existing payment or Creating a payment for the invoice
            if Payments.objects.filter(invoice=invoice).exists():
                payment = Payments.objects.get(invoice=invoice)
                if paid_amount is not None:
                    payment.payment_ammount += float(paid_amount)
                payment.transaction_id = val_id,
                payment.payment_method = 'SSLCOMMERZ'
                payment.payment_date = date.today()
                payment.payment_note = ""
                payment.save()
            else:
                payment = Payments.objects.create(
                    invoice=invoice,
                    title=invoice.number + " Payment",
                    payment_method='SSLCOMMERZ',
                    payment_ammount=paid_amount,
                    transaction_id=val_id,
                    payment_date=date.today(),
                    payment_note="",
                )

            messages.success(request, 'Payment successful!')
            redirect_url = reverse('inv_payment_confirmation', args=[invoice.slug]) + '?first_visit=true&paid_amount=' + paid_amount
            return redirect(redirect_url)

    return redirect('viewUserPDFInvoice', slug=invoice.slug)


@csrf_exempt
def inv_sslc_failed(request):
    if request.POST:
        messages.warning(request, 'Payment failed!')
        return redirect('payment_failed')
