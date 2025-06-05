from django.utils.text import slugify
from .models import UserProfile
from django.conf import settings
import uuid
from django.core.mail import send_mail
from django.utils import timezone
from .models import PasswordResetToken
from django.urls import reverse
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from apps.settings.models import websiteSetting
from django.contrib import messages


def create_user_profile(user):
    UserProfile.objects.create(
        user=user,
        email=user.email,
        name=user.username,
        slug=slugify(user.username),
    )


def generate_reset_token_and_send_email(user, request):
    token = uuid.uuid4()  # Generate a UUID4 token
    expiration_time = timezone.now() + timezone.timedelta(hours=1) 
    reset_token = PasswordResetToken.objects.create(user=user, token=token, expiration_time=expiration_time)

    reset_link = request.build_absolute_uri(reverse('reset_password', args=[str(reset_token.token)]))
    
    website_settings = websiteSetting.objects.first()
    try:
        subject = "Password Reset"
        html_message = render_to_string('admin/auth/email/password_reset_email.html', {
            'user': user,
            'reset_link': reset_link,
        })
        plain_message = strip_tags(html_message) 
        from_email = f'"{website_settings.name}" <{settings.EMAIL_HOST_USER}>'
        recipient_list = [user.email]

        # Send the email with HTML content
        send_mail(subject, plain_message, from_email, recipient_list, html_message=html_message)
        return messages.success(request, 'An email has sent!')
    except:
        return messages.warning(request, 'Something went wrong!')
