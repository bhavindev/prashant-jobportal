from sslcommerz_lib import SSLCOMMERZ
from apps.settings.models import *
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect, get_object_or_404
from apps.order.models import *
from django.contrib import messages
from django.urls import reverse
from apps.crm.models import Invoice, crmProjects, InvoiceItem, Payments
from uuid import uuid4
from datetime import date


def sslCommerzGateway(name, email, price, phone, address, city, country, user, host, protocol):
    credential = paymentMethod.objects.first()
    web_settings = websiteSetting.objects.first()
    settings = {'store_id': credential.ssl_commerze_store_id, 'store_pass': credential.ssl_commerze_store_pass,
                'issandbox': credential.ssl_commerze_is_sandbox}
    sslcommez = SSLCOMMERZ(settings)

    post_body = {
        'total_amount': price,
        'currency': str(web_settings.currency_name),
        'tran_id': "12345",
        'cancel_url': f"{protocol}://{host}/order/sslcommerze/failed",
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
        "success_url": f"{protocol}://{host}/order/sslcommerze/success",
        'fail_url': f"{protocol}://{host}/order/sslcommerze/failed",
        "value_a": user

    }

    response = sslcommez.createSession(post_body)

    return response


@csrf_exempt
def sslcommerze_success(request):
    order_settings = websiteSetting.objects.first()

    if request.POST:
        val_id = request.POST.get('val_id')
        user = request.POST.get('value_a')
        order = get_object_or_404(Order, user=user, is_ordered=False)
        
        price = 0
        if order.promo:
            price = order.total_amount_after_discount
        else:
            price = order.total_amount
            
        number = 'INV-' + str(uuid4()).split('-')[1]
        if val_id:
            order.payment_method = 'ssl_commerz'
            order.is_ordered = True
            order.status = "confirmed"
            order.transaction_id = val_id
            order.save()

            if order_settings.is_auto_invoice_enable:

                # Creating a project for the invoice
                project = crmProjects.objects.create(
                    title=f"Project of Order {order.order_id}",
                    start_date=date.today(),
                    deadline=date.today(),
                    price=price,
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
                    discount_amount=order.total_amount - order.total_amount_after_discount,
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

                invoice.save()

                # Creating a payment for the invoice
                payment_method_mapping = {
                    'ssl_commerz': 'SSLCOMMERZ',
                }
                readable_payment_method = payment_method_mapping.get(order.payment_method, order.payment_method)
                payment = Payments.objects.create(
                    invoice=invoice,
                    title=f"Invoice #{number} Payment",
                    payment_method=readable_payment_method,
                    transaction_id=val_id,
                    payment_ammount=price,
                    payment_date=date.today(),
                    payment_note="Your Payment Note",
                )

            messages.success(request, 'Order placed successfully!')
            redirect_url = reverse('order_confirmation', args=[order.id]) + '?first_visit=true'
            return redirect(redirect_url)

    return redirect('checkout')


@csrf_exempt
def sslcommerze_failed(request):
    if request.POST:
        messages.warning(request, 'Payment failed!')
        return redirect('payment_failed')
