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


def paypalGeteway(price, host, protocol):
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
            "return_url": f"{protocol}://{host}/order/paypal/success",
            "cancel_url": f"{protocol}://{host}/order/paypal/failed"},
        "transactions": [{
            "amount": {
                "total": f"{price}",
                "currency": str(web_settings.currency_name)},
            "description": ""}]})
    print(payment)
    if payment.create():

        for link in payment.links:
            if link.rel == "approval_url":
                approval_url = str(link.href)

                return approval_url
    else:
        print(payment.errors)


@csrf_exempt
def paypal_success(request):
    paymentID = request.GET.get('paymentId')
    user = request.user
    order = get_object_or_404(Order, user=user, is_ordered=False)
    order_settings = websiteSetting.objects.first()
    number = 'INV-' + str(uuid4()).split('-')[1]

    if paymentID:
        order.payment_method = 'paypal'
        order.is_ordered = True
        order.status = "confirmed"
        order.transaction_id = paymentID
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
                'paypal': 'Paypal',
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
def paypal_failed(request):
    messages.warning(request, 'Payment failed!')
    return redirect('payment_failed')
