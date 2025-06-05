from apps.settings.models import paymentMethod

def payment_method_context(request):
    method = paymentMethod.objects.first()
    return {'method' : method}
