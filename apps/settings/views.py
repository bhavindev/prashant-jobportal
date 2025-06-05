from django.shortcuts import render, get_object_or_404, redirect
from apps.settings.models import websiteSetting, paymentMethod, PromotionalBanner
from apps.settings.forms import openaiSettingsForm, paymentMethodsForm, PromotionalBannerForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from core.decorators import admin_role_required

# Openai settings
@login_required(login_url='signIn')
@admin_role_required
def adminOpenaiSettings(request):
    openai_settings = websiteSetting.objects.first()
    form = openaiSettingsForm(instance=openai_settings)
    
    if request.method == 'POST':
        form = openaiSettingsForm(request.POST, instance=openai_settings)
        if form.is_valid():
            form.save()
            messages.success(request, 'OpenAI Configured Successfully!')
            return redirect('adminOpenaiSettings')
        
    context = {
        'title' : 'OpenAI Settings',
        'form' : form,
        'openai_settings' : openai_settings
    }
    
    return render(request, 'admin/front/main/settings/ai.html', context)

# Payment methods settings
@login_required(login_url='signIn')
@admin_role_required
def adminPaymentMethodsSettings(request):
    payment_methods = paymentMethod.objects.first()
    form = paymentMethodsForm(instance=payment_methods)
    
    if request.method == 'POST':
        form = paymentMethodsForm(request.POST, instance=payment_methods)
        if form.is_valid():
            form.save()
            messages.success(request, 'Updated Successfully!')
            return redirect('adminPaymentMethodsSettings')
    
    context = {
        'title' : 'Payment Methods',
        'form' : form,
        'payment_methods' : payment_methods
    }
    
    return render(request, 'admin/front/main/settings/payment_methods.html', context)
        

# Error Page
def error_404(request, exception):
    return render(request, 'error/error_404.html', status=404)
