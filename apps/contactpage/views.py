from django.shortcuts import render, redirect, get_object_or_404
from apps.contactpage.models import *
from apps.adminapp.forms import ContactForm
from django.contrib import messages
from django.http import JsonResponse
from apps.contactpage.models import Subscriber
from apps.contactpage.forms import SubscriberForm ,EmailSelectForm
from django.contrib import messages
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.decorators import login_required


def contactPageFront(request):
    # Get the default language
    default_language = Languages.objects.filter(is_default=True).first()
    
    # Get the selected language from session or use default language
    selected_language_code = request.session.get('selected_language', default_language.code)
    
    meta = ContactPageSEO.objects.filter(language__code=selected_language_code).first()
    info = ContactInfo.objects.filter(language__code=selected_language_code).first()
    form = ContactForm()
    
    if request.method == 'POST':
        if 'name' in request.POST:
            form = ContactForm(request.POST, request.FILES)
            if form.is_valid():
                print(form.cleaned_data)
                form.save()
                messages.success(request, 'Submitted successfully! We will get back to you soon.')
                return redirect('contactPageFront')
        else:
            selected_language_code = request.POST.get('language', default_language.code)
            request.session['selected_language'] = selected_language_code
            return redirect('contactPageFront')
    
    context = {
        'meta' : meta,
        'info' : info,
        'form' : form,
    }
        
    return render(request, 'front/main/contact.html', context)

# Subscriber Views
def ajax_subscribe(request):
    if request.method == "POST" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
         # Check if there's a session variable for the last submission time
        last_submission_time_str = request.session.get('last_contact_submission_time')

        if last_submission_time_str:
            # Convert the stored time string back to a datetime object
            last_submission_time = datetime.fromisoformat(last_submission_time_str)

            # Calculate the time difference between the last submission and the current time
            time_difference = timezone.now() - last_submission_time

            # Check if less than five minutes have passed since the last submission
            if time_difference.total_seconds() < 300:  # 300 seconds = 5 minutes
                # Calculate the time left for the next submission
                time_left_seconds = 300 - time_difference.total_seconds()
                minutes_left = int(time_left_seconds / 60)
                seconds_left = int(time_left_seconds % 60)

                return JsonResponse({'status': 'error', 'message': f'You can subscribe again in {minutes_left} minutes and {seconds_left} seconds.'})

        # Save the current time in the session as a string in ISO 8601 format
        request.session['last_contact_submission_time'] = timezone.now().isoformat()

        form = SubscriberForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success', 'message': 'Subscription successful!'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid email or email already exists!'})
        
    return JsonResponse({'status': 'error', 'message': 'Invalid method or not an AJAX request!'})

# Subscriber Admin
@login_required(login_url='signIn')
def subscriberViewAdmin(request):
    
    subscribers = Subscriber.objects.all()
    
    context = {
        'title' : 'Subscribers',
        'subscribers' : subscribers
        
    }
    return render(request, 'admin/front/main/pages/partial/subscribers.html', context)

@login_required(login_url='signIn')
def subscriberDelete(request, id):
    subscriber = get_object_or_404(Subscriber , id=id)
    subscriber.delete()
    messages.warning(request, 'Subscriber deleted!')
    return redirect('subscriberViewAdmin')



# Error Page
def error_404(request, exception):
    return render(request, 'error/error_404.html', status=404)

