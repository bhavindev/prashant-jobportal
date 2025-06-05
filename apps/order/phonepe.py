# from phonepe.sdk.pg.payments.v1.payment_client import PhonePePaymentClient
# from phonepe.sdk.pg.env import Env
# from phonepe.sdk.pg.payments.v1.models.request.pg_pay_request import PgPayRequest
# import uuid
# from django.shortcuts import redirect, get_object_or_404
# from django.views.decorators.csrf import csrf_exempt
# from apps.crm.models import crmProjects, Payments, Invoice, InvoiceItem
# from datetime import date
# from django.contrib import messages
# from apps.settings.models import paymentMethod, websiteSetting
# from apps.order.models import *
# from uuid import uuid4
# from django.urls import reverse

# def PhonepeGateway(price, protocol, host, request):
#     merchant_id = "SAKIBSIRAJONLINE"
#     salt_key = "df27fbfe-dc48-46b0-bae5-7a96bab9fbe3"
#     salt_index = 1
#     env = Env.PROD

#     phonepe_client = PhonePePaymentClient(merchant_id=merchant_id, salt_key=salt_key, salt_index=salt_index, env=env)

#     unique_transaction_id = str(uuid.uuid4())[:-2]
#     s2s_callback_url = f"{protocol}://{host}/order/phonepe/success/"
#     amount = price*100
#     id_assigned_to_user_by_merchant = str(request.user.pk)

#     pay_page_request = PgPayRequest.pay_page_pay_request_builder(
#         merchant_transaction_id=unique_transaction_id,
#         amount=amount,
#         merchant_user_id=id_assigned_to_user_by_merchant,
#         callback_url=s2s_callback_url
#     )

#     print(f"Debug: Merchant ID - {merchant_id}, Salt Key - {salt_key}, Callback URL - {s2s_callback_url}")

#     try:
#         pay_page_response = phonepe_client.pay(pay_page_request)
#         print(f"Debug: Pay Page Response - {pay_page_response}")
#         pay_page_url = pay_page_response.data.instrument_response.redirect_info.url
#         return pay_page_url
#     except Exception as e:
#         print(f"Error: {e}")
#         return "/error-page/" 

# @csrf_exempt
# def phonepe_success(request):
#     paymentID = request.GET.get('paymentId')
#     user = request.user
#     order = get_object_or_404(Order, user=user, is_ordered=False)
#     order_settings = websiteSetting.objects.first()
#     number = 'INV-' + str(uuid4()).split('-')[1]

#     if paymentID:
#         order.payment_method = 'phonepe'
#         order.is_ordered = True
#         order.status = "confirmed"
#         order.transaction_id = paymentID
#         order.save()

#         if order_settings.is_auto_invoice_enable:

#             # Creating a project for the invoice
#             project = crmProjects.objects.create(
#                 title=f"Project of Order {order.order_id}",
#                 start_date=date.today(),
#                 deadline=date.today(),
#                 price=order.total_amount,
#                 client=order.user,
#                 label='started',
#             )

#             # Creating an invoice for the user
#             invoice = Invoice.objects.create(
#                 number=number,
#                 client=order.user,
#                 billDate=date.today(),
#                 dueDate=date.today(),
#                 project=project,
#                 title=f"Invoice for Order {order.order_id}",
#                 sub_total=order.total_amount,
#                 discount_amount=0,
#                 tax_amount=0,
#                 other_fees_name="Other Fees",
#                 other_fees_amount=0,
#             )
#             invoice.products.set(order.products.all())

#             # Adding invoice items based on order products
#             for cart_item in Cart.objects.filter(order=order):
#                 invoice_item = InvoiceItem.objects.create(
#                     invoice=invoice,
#                     item=cart_item.product,
#                     unit_type=cart_item.unit_type,
#                     quantity=cart_item.quantity,
#                     unit_price=cart_item.unit_price,
#                     sub_total=cart_item.subtotal,
#                 )

#             invoice.sub_total = invoice.get_total()
#             invoice.save()

#             # Creating a payment for the invoice
#             payment_method_mapping = {
#                 'phonepe': 'PhonePE',
#             }
#             readable_payment_method = payment_method_mapping.get(order.payment_method, order.payment_method)
#             payment = Payments.objects.create(
#                 invoice=invoice,
#                 title=f"Invoice #{number} Payment",
#                 payment_method=readable_payment_method,
#                 payment_ammount=invoice.sub_total,
#                 payment_date=date.today(),
#                 payment_note="Your Payment Note",
#             )

#         messages.success(request, 'Order placed successfully!')
#         redirect_url = reverse('order_confirmation', args=[order.id]) + '?first_visit=true'
#         return redirect(redirect_url)
#     else:
#         return redirect('checkout')


# @csrf_exempt
# def phonepe_failed(request):
#     messages.warning(request, 'Payment failed!')
#     return redirect('payment_failed')