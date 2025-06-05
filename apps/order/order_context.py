from apps.order.models import *

def user_cart_context(request):
    try:
        user_order = None
        user_cart = None

        if request.user.is_authenticated:
            user_order = Order.objects.get(user=request.user, is_ordered=False)
            user_cart = Cart.objects.filter(order=user_order)

    except Order.DoesNotExist:
        pass 

    return {'user_cart': user_cart, 'user_order': user_order}
