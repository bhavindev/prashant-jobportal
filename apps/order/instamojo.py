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


def mojoGetaway(request, price, email, host, protocol):
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
            redirect_url=f"{protocol}://{host}/order/instamojo/success",
        )

        paymentID = response['payment_request']['id']
        print(response)

        request.session['instamojo_paymentID'] = paymentID

        return response['payment_request']['longurl']
    except KeyError as e:
        print(f"KeyError: {e}. Response from Instamojo: {response}")
        return None
    

@csrf_exempt
def instamojo_success(request):
    paymentID = request.session.get('instamojo_paymentID')
    user = request.user
    order = get_object_or_404(Order, user=user, is_ordered=False)
    order_settings = websiteSetting.objects.first()
    number = 'INV-' + str(uuid4()).split('-')[1]

    if paymentID:
        order.payment_method = 'instamojo'
        order.is_ordered = True
        order.status = "confirmed"
        order.transaction_id = paymentID
        order.save()
        del request.session['instamojo_paymentID']

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
                'instamojo': 'Instamojo',
            }
            readable_payment_method = payment_method_mapping.get(order.payment_method, order.payment_method)
            payment = Payments.objects.create(
                invoice=invoice,
                title=f"Invoice #{number} Payment",
                transaction_id=paymentID,
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

@csrf_exempt
def instamojo_failed(request):
    messages.warning(request, 'Payment failed!')
    return redirect('payment_failed')