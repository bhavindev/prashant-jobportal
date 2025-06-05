# from django.http import JsonResponse
# import razorpay
# from django.views.decorators.csrf import csrf_exempt
# from django.shortcuts import redirect, render, get_object_or_404
# from apps.order.models import *
# from django.contrib import messages
# from django.urls import reverse
# from apps.settings.models import paymentMethod, websiteSetting

# @csrf_exempt
# def razorpayGetaway(request, price):
#     credential = paymentMethod.objects.first()
#     web_settings = websiteSetting.objects.first()
#     if request.method == 'POST':
#         client = razorpay.Client(auth=(credential.razorpay_api_key, credential.razorpay_api_secret))
#         amount = int(price * 100) 

#         order_data = {
#             'amount': amount,
#             'currency': 'INR',
#             'payment_capture': 1,
#         }
#         order = client.order.create(order_data)

#         return JsonResponse({'order_id': order['id'], 'amount': order['amount']})
#     else:
#         return JsonResponse({'error': 'Invalid request method'})
    
# @csrf_exempt
# def razorpay_success(request):
#     razorpay_payment_id = request.GET.get('razorpay_payment_id')
    
#     user = request.user
#     order = get_object_or_404(Order, user=user, is_ordered=False)
    
#     if razorpay_payment_id:
#         order.payment_method = 'razorpay'
#         order.is_ordered = True
#         order.status = "confirmed"
#         order.transaction_id = razorpay_payment_id
#         order.save()
        
#         messages.success(request, 'Order placed successfully!')
        
#         redirect_url = reverse('order_confirmation', args=[order.id]) + '?first_visit=true'
#         return redirect(redirect_url)
#     else:
#         return redirect('checkout')