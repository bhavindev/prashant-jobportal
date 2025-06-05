import requests
import json
import uuid
from datetime import date
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.urls import reverse
from apps.order.models import *
from apps.settings.models import paymentMethod, websiteSetting
from apps.crm.models import Invoice, Payments


def paymobGateway(user, host, protocol, price, billing_data, items, slug):
    try:
        credential = paymentMethod.objects.first()
        web_settings = websiteSetting.objects.first()
        
        special_reference = str(uuid.uuid4())

        intention_url = "https://accept.paymob.com/v1/intention/"
        unified_checkout_url= "https://accept.paymob.com/unifiedcheckout/?publicKey={}&clientSecret={}"
        
        payload = json.dumps({
            "amount": price * 100,
            "currency": "EGP",
            "expiration": 3600,
            "payment_methods": [int(credential.paymob_integration_id)],
            "items": items,
            "billing_data": billing_data,
            "special_reference": special_reference,
            "notification_url": f'{protocol}://{host}/order/paymob/notification',
            "redirection_url": f'{protocol}://{host}/order/paymob/success?user_id={user.id}&slug={slug}&price={price}',
            "extras": {"ee": 22}
        })

        headers = {
            'Authorization': f'Token {credential.paymob_secret_key}',
            'Content-Type': 'application/json'
        }

        response = requests.post(intention_url, headers=headers, data=payload)

        if response.status_code == 201:
            data = response.json()
            client_secret = data.get("client_secret")
            if client_secret:
                checkout_url = unified_checkout_url.format(credential.paymob_public_key, client_secret)
                return checkout_url
        else:
            print(f"Failed to create payment intention. Status Code: {response.status_code}")
            print(response.text)
            return None
    except Exception as e:
        print(f"Failed to create payment intention. Error: {e}")
        return None


@csrf_exempt
def paymob_success(request):
    
    user_id = request.GET.get('user_id')
    is_pending = request.GET.get('pending')
    transaction_id = request.GET.get('id')
    slug = request.GET.get('slug')
    invoice = get_object_or_404(Invoice, slug=slug)
    paid_amount = request.GET.get('price')

    if user_id and is_pending == "false" and transaction_id:
        invoice.status = "PAID"
        invoice.save()
        
        if Payments.objects.filter(invoice=invoice).exists():
            payment = Payments.objects.get(invoice=invoice)
            if paid_amount is not None:
                payment.payment_ammount += float(paid_amount)
            payment.transaction_id = transaction_id,
            payment.payment_method = 'Paymob'
            payment.payment_date = date.today()
            payment.payment_note = ""
            payment.save()
            
        else:
            payment = Payments.objects.create(
                invoice=invoice,
                title=invoice.number + " Payment",
                payment_method='Paymob',
                payment_ammount=paid_amount,
                transaction_id=transaction_id,
                payment_date=date.today(),
                payment_note="",
            )
            
        messages.success(request, 'Payment successful!')
        redirect_url = reverse('inv_payment_confirmation', args=[invoice.slug]) + '?first_visit=true&paid_amount=' + paid_amount
        return redirect(redirect_url)
        

    return redirect('viewUserPDFInvoice', slug=invoice.slug)