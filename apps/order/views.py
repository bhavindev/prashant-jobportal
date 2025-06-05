from django.shortcuts import render, redirect, get_object_or_404
from uuid import uuid4
from apps.crm.models import crmProjects, Invoice, InvoiceItem
from datetime import date
from apps.order.models import *
from django.contrib import messages
from apps.order.sslcommerze_pay import sslCommerzGateway
from apps.order.paypal import paypalGeteway
from apps.order.stripe import stripeGateway
# from apps.order.razorpay import razorpayGetaway
from apps.order.instamojo import mojoGetaway
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import JsonResponse
from apps.settings.models import websiteSetting
from apps.crm.forms import invoiceForm
from django.http import HttpResponseRedirect
from apps.order.paymob import paymobGateway


"""Product list"""
@login_required(login_url='signIn')
def product_list(request):
    order_settings = websiteSetting.objects.first()
    if order_settings.is_purchasing_enable:
        products = items.objects.all().order_by("-id")
        return render(request, 'user/main/ecom/products.html', {'products': products})
    else:
        return redirect('userDashboard')


"""Add to cart"""
@login_required(login_url='signIn')
def add_to_cart(request, product_id):
    order_settings = websiteSetting.objects.first()
    if order_settings.is_purchasing_enable:
        product = items.objects.get(pk=product_id)
        order, created = Order.objects.get_or_create(user=request.user, is_ordered=False)

        user_quantity = int(request.POST.get('user_quantity', 1))

        order_product, created = Cart.objects.get_or_create(order=order, product=product)

        if created:
            order_product.quantity = user_quantity
            messages.success(request, f'{product} added to cart successfully!')
        else:
            order_product.quantity += user_quantity
            messages.info(request, f'Quantity updated successfully for {product}!')

        if product.rate is not None:
            order_product.unit_price = product.rate
            order_product.subtotal += product.rate * user_quantity
            order_product.unit_type = product.unit_type
            order.total_amount += product.rate * user_quantity
            order.save()

        order_product.save()
        order.products.add(product)

        return redirect('product_list')
    else:
        return redirect('userDashboard')

"""Cart view"""

@login_required(login_url='signIn')
def view_cart(request):
    order_settings = websiteSetting.objects.first()
    if order_settings.is_purchasing_enable:
        return render(request, 'user/main/ecom/cart.html')
    else:
        return redirect('userDashboard')

@login_required(login_url='signIn')
def cart_delete(request, id):
    order_settings = websiteSetting.objects.first()
    if order_settings.is_purchasing_enable:
        cart_item = get_object_or_404(Cart, pk=id)

        if cart_item.order.user != request.user:
            messages.warning(request, "You do not have permission to delete this item.")
            return redirect('view_cart')

        cart_item.order.products.remove(cart_item.product)
        cart_item.order.total_amount -= cart_item.subtotal
        cart_item.order.save()

        cart_item.delete()
        if cart_item.order.products.count() == 0:
            cart_item.order.delete()
        messages.warning(request, f'{cart_item.product.name} is deleted from cart!')
        return redirect('view_cart')
    else:
        return redirect('userDashboard')


"""Checkout"""

@login_required(login_url='signIn')
def checkout(request):
    order_settings = websiteSetting.objects.first()
    if order_settings.is_purchasing_enable:
        current_host = request.get_host()
        protocol = 'https' if request.is_secure() else 'http'
        number = 'INV-' + str(uuid4()).split('-')[1]

        if request.user.is_authenticated:
            try:
                order = Order.objects.get(user=request.user, is_ordered=False)
                if order.promo:
                    price = order.total_amount_after_discount
                else:
                    price = order.total_amount
            except Order.DoesNotExist:
                return redirect('view_cart')

            if request.method == 'POST':
                form = invoiceForm()
                if form.is_valid():
                    form.save()

            if request.method == 'POST':
                name = request.POST.get('name')
                email = request.POST.get('email')
                phone = request.POST.get('phone')
                city = request.POST.get('city')
                address = request.POST.get('address')
                country = request.POST.get('country')
                postal = request.POST.get('zipcode')

                if not all([name, email, phone, city, address, country]) and 'coupon_code' not in request.POST and 'remove_coupon' not in request.POST:
                    messages.warning(request, 'Billing information is required! Please add from profile.')
                    return render(request, 'user/main/ecom/checkout.html', {'order': order})
                
                if 'coupon_code' in request.POST:
                    code = request.POST.get('coupon_code')
                    promo = PromoCode.objects.filter(code=code, is_active=True).first()

                    if promo is not None:
                        existing_order_with_promo = Order.objects.filter(user=request.user, promo=promo, is_ordered=True).exists()

                        if promo.min_purchase and promo.min_purchase > 0.0:
                            if promo.min_purchase > order.total_amount:
                                messages.warning(request, f'You need to purchase minimum {order_settings.currency_symbol}{promo.min_purchase} to use this promo code.')
                                return redirect('checkout')
                            
                        if existing_order_with_promo:
                            messages.warning(request, 'You have already used this promo code on a previous order.')
                            return redirect('checkout')

                        if request.user not in promo.user_applied.all():
                            if order.promo:
                                old_promo = order.promo
                                if request.user in old_promo.user_applied.all():
                                    old_promo.user_applied.remove(request.user)

                            order.promo = promo

                            if order.promo.discount_type == 'Percentage':
                                order.total_amount_after_discount = order.total_amount - (order.total_amount * promo.discount / 100)
                                order.total_amount_after_discount = round(order.total_amount_after_discount, 2)
                            elif order.promo.discount_type == 'Fixed':
                                order.total_amount_after_discount = order.total_amount - promo.discount
                            else:
                                order.total_amount_after_discount = order.total_amount

                            promo.user_applied.add(request.user)
                            order.save()

                            discount_applied = order.total_amount - order.total_amount_after_discount
                            messages.success(request, f'Promo code applied successfully! Discount: {order_settings.currency_symbol}{discount_applied}')
                            
                            return redirect('checkout')

                        else:
                            messages.warning(request, 'Promo code already used!')
                            return redirect('checkout')
                    else:
                        messages.warning(request, 'Invalid promo code!')
                        return redirect('checkout')

                
                elif 'remove_coupon' in request.POST:
                    order.promo.user_applied.remove(request.user)
                    order.promo = None
                    order.total_amount_after_discount = 0
                    order.save()
                    messages.info(request, 'Promo code removed successfully!')
                    return redirect('checkout')


                elif 'sslcommerze' in request.POST:
                    response = sslCommerzGateway(name=name, email=email, price=price, phone=phone,
                                                address=address, city=city, country=country, user=request.user.pk,
                                                host=current_host, protocol=protocol)
                    if response['status'] == 'SUCCESS':
                        redirect_url = response['GatewayPageURL']
                        return redirect(redirect_url)
                    else:
                        print(response)
                        return redirect('view_cart')

                elif 'paypal' in request.POST:
                    paypal_url = paypalGeteway(price=price, host=current_host, protocol=protocol)
                    return redirect(paypal_url)

                elif 'instamojo' in request.POST:
                    mojo_url = mojoGetaway(request, price=price, email=email, protocol=protocol, host=current_host)

                    if mojo_url is not None:
                        return redirect(mojo_url)
                    else:
                        print("Error: Instamojo payment processing failed.")
                
                # elif 'phonepe' in request.POST:
                #     price = order.total_amount
                #     phonepe_url = PhonepeGateway(price=price, protocol=protocol, host=current_host, request=request)
                #     return HttpResponseRedirect(phonepe_url)
                
                elif 'stripe' in request.POST:
                    gateway_url = stripeGateway(host=current_host, protocol=protocol, price=price)
                    return redirect(gateway_url)
                

                elif 'paymob' in request.POST:
                    name_parts = name.split()

                    if len(name_parts) > 1:
                        first_name = name_parts[0]
                        last_name = " ".join(name_parts[1:])
                    else:
                        first_name = name_parts[0]
                        last_name = ""  
                        
                    billing_data = {
                        "apartment": address,
                        "email": email,
                        "floor": "",
                        "first_name": first_name,
                        "last_name": last_name,
                        "street": address,
                        "building": "",
                        "phone_number": phone,
                        "shipping_method": "",
                        "postal_code": postal,
                        "city": city,
                        "country": country
                    }
                    items = []
                    cart_items = Cart.objects.filter(order=order)
                    for cart_item in cart_items:
                        item_data = {
                            "name": cart_item.product.name,
                            "amount": int(cart_item.unit_price * 100),
                            "description": "",
                            "quantity": cart_item.quantity
                        }
                        items.append(item_data)
                    payment_url = paymobGateway(user=request.user, host=current_host, protocol=protocol, price=price, billing_data=billing_data, items=items)
                    return redirect(payment_url)

                # elif 'razorpay' in request.POST:
                #     # Get Razorpay order details
                #     response = razorpayGetaway(request, price=order.total_amount)
                #     if 'order_id' in response and 'amount' in response:
                #         order.payment_method = 'razorpay'
                #         order.save()

                #         return JsonResponse(response)
                #     else:
                #         print(response)
                #         return redirect('view_cart')

                elif 'offlinepayment' in request.POST:
                    order.payment_method = 'offlinepayment'
                    order.is_ordered = True
                    order.status = "pending"
                    order.transaction_id = "Offline Payment"
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
                            InvoiceItem.objects.create(
                                invoice=invoice,
                                item=cart_item.product,
                                unit_type=cart_item.unit_type,
                                quantity=cart_item.quantity,
                                unit_price=cart_item.unit_price,
                                sub_total=cart_item.subtotal,
                            )

                        invoice.sub_total = invoice.get_total()
                        invoice.save()

                    messages.success(request, 'Order placed successfully!')
                    redirect_url = reverse('order_confirmation', args=[order.id]) + '?first_visit=true'
                    return redirect(redirect_url)

                else:
                    pass

            return render(request, 'user/main/ecom/checkout.html', {'order': order})
        else:
            return redirect('signIn')
    else:
        return redirect('userDashboard')


@login_required(login_url='signIn')
def order_confirmation(request, id):
    order = get_object_or_404(Order, id=id, user=request.user, is_ordered=True)

    first_visit = request.GET.get('first_visit', None)

    if first_visit:
        cart_items = Cart.objects.filter(order=order)
        return render(request, 'user/main/ecom/order_confirm.html', {'order': order, 'cart_items': cart_items})

    return redirect('product_list')


@login_required(login_url='signIn')
def payment_failed(request):
    return render(request, 'user/main/ecom/payment-fail.html')
