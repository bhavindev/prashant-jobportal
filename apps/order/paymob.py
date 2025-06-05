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
from apps.authapp.models import User
from apps.crm.models import Invoice, crmProjects, InvoiceItem, Payments


def paymobGateway(user, host, protocol, price, billing_data, items):
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
            "redirection_url": f'{protocol}://{host}/order/paymob/success?user_id={user.id}',
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
    order_settings = websiteSetting.objects.first()

    # Extract data from GET request
    user_id = request.GET.get('user_id')
    is_pending = request.GET.get('pending')
    transaction_id = request.GET.get('id')

    if user_id and is_pending == "false" and transaction_id:
        user = get_object_or_404(User, id=user_id)
        order = get_object_or_404(Order, user=user, is_ordered=False)
        
        order.payment_method = 'paymob'
        order.is_ordered = True
        order.status = "confirmed"
        order.transaction_id = transaction_id
        order.save()

        if order_settings.is_auto_invoice_enable:
            project = crmProjects.objects.create(
                title=f"Project of Order {order.order_id}",
                start_date=date.today(),
                deadline=date.today(),
                price=order.total_amount,
                client=order.user,
                label='started',
            )

            number = 'INV-' + str(uuid.uuid4()).split('-')[1]

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

            payment_method_mapping = {
                'paymob': 'Paymob',
            }
            readable_payment_method = payment_method_mapping.get(order.payment_method, order.payment_method)
            payment = Payments.objects.create(
                invoice=invoice,
                title=f"Invoice #{number} Payment",
                payment_method=readable_payment_method,
                transaction_id=transaction_id,
                payment_ammount=invoice.sub_total,
                payment_date=date.today(),
                payment_note="Paymob payment",
            )

        messages.success(request, 'Order placed successfully!')
        redirect_url = reverse('order_confirmation', args=[order.id]) + '?first_visit=true'
        return redirect(redirect_url)

    return redirect('checkout')