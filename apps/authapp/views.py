from django.shortcuts import render, redirect, get_object_or_404
from apps.authapp.models import *
from apps.authapp.forms import *
from django.contrib.auth import authenticate, login, logout
from apps.authapp.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.http import Http404
from django.contrib import messages
from core.decorators import admin_role_required, both_role_required
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from apps.settings.models import websiteSetting, HeaderFooter
from django.urls import reverse
from apps.authapp.utils import generate_reset_token_and_send_email
# Users List


@login_required(login_url='signIn')
@admin_role_required
def usersList(request):
    users = UserProfile.objects.all()
    messages_data = messages.get_messages(request)
    context = {
        'title': 'Users',
        'users': users,
        'messages': messages_data
    }
    return render(request, 'admin/auth/user/users.html', context)


@login_required(login_url='signIn')
@admin_role_required
def createUser(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Prevent immediate save
            user.role = form.cleaned_data['role']  # Set role from form
            user.save()  # Save User instance to DB
            messages.success(request, 'User created successfully!')

            # Update or Create a profile for the user
            UserProfile.objects.update_or_create(
                user=user,
                defaults={
                    'name': form.cleaned_data['name'],
                    'email': form.cleaned_data['email']
                }
            )

            # Send a welcome email to the user
            try:
                website_settings = websiteSetting.objects.first()
                header_footer = HeaderFooter.objects.first()
                contact_url = request.build_absolute_uri(
                    reverse('contactPageFront'))
                subject = f'Welcome to {website_settings.name}'
                from_email = f'"{website_settings.name}" <{settings.DEFAULT_FROM_EMAIL}>'
                to_email = [form.cleaned_data['email']]

                # Load the HTML email template
                html_message = render_to_string('admin/auth/email/welcome.html', {
                    'username': form.cleaned_data['username'],
                    'settings': website_settings,
                    'footer': header_footer,
                    'contact': contact_url
                })

                email_message = EmailMessage(
                    subject=subject,
                    body=html_message,
                    from_email=from_email,
                    to=to_email,
                )
                email_message.content_subtype = 'html'
                email_message.send()
            except Exception as e:
                pass

            return redirect('users')
        else:
            print(form.errors)
    else:
        form = CustomUserCreationForm()

    context = {
        'title': 'Create User',
        'form': form,
    }
    return render(request, 'admin/auth/user/create.html', context)

# Edit User


@login_required(login_url='signIn')
def editUserProfile(request, slug):
    try:
        profile = UserProfile.objects.get(slug=slug)
        user = profile.user
    except UserProfile.DoesNotExist:
        raise Http404("User profile does not exist")

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('editProfile', profile.slug)
    else:
        form = UserProfileForm(instance=profile)

    context = {
        'title': 'Edit User Profile',
        'form': form,
        'profile': profile,
        'user': user,
    }
    return render(request, 'admin/auth/user/edit.html', context)

# Change Password


@login_required(login_url='signIn')
def changePassword(request, username):

    user = User.objects.get(username=username)
    profile = UserProfile.objects.get(user=user)

    if request.method == 'POST':
        form = UserPasswordChangeForm(user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password changed successfully.')
            return redirect('users')
    else:
        form = UserPasswordChangeForm(user)

    context = {
        'title': 'Change Password',
        'form': form,
        'profile': profile,
        'user': user,
    }
    return render(request, 'admin/auth/user/changepassword.html', context)

# User Delete


@login_required(login_url='signIn')
@admin_role_required
def delete_user(request, username):
    user = get_object_or_404(User, username=username)

    # Retrieve the user object or raise 404 exception if not found
    user = get_object_or_404(User, username=username)
    # Delete the user
    user.delete()
    messages.warning(request, 'User delete!')

    # Redirect to a success page or any desired URL
    return redirect('users')

# User Profile


@login_required(login_url='signIn')
@both_role_required
def userProfile(request):
    user_profile = UserProfile.objects.get(user=request.user)

    context = {
        'title': 'User Profile',
        'profile': user_profile
    }
    return render(request, 'admin/auth/user/userProfile.html', context)

# Sign Up/Registration


def SignUp(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('login[password]')
        email = request.POST.get('email')
        if Guser.objects.filter(username__iexact=username):
            messages.warning(request, 'Username already exists')
            return redirect('signUp')
        if Guser.objects.filter(email__iexact=email):
            messages.warning(request, 'Email already exists')
            return redirect('signUp')
        user = Guser.objects.create_user(
            username=username,  email=email, password=password)
        if user:
            UserProfile.objects.update_or_create(
                user=user,
                defaults={
                    'name': username,
                    'email': email,
                }
            )
            try:
                # Send a welcome email to the user
                website_settings = websiteSetting.objects.first()
                header_footer = HeaderFooter.objects.first()
                contact_url = request.build_absolute_uri(
                    reverse('contactPageFront'))
                subject = f'Welcome to {website_settings.name}'
                from_email = f'"{website_settings.name}" <{settings.DEFAULT_FROM_EMAIL}>'
                to_email = [email]

                # Load the HTML email template
                html_message = render_to_string('admin/auth/email/welcome.html', {
                    'username': username,
                    'settings': website_settings,
                    'footer': header_footer,
                    'contact': contact_url

                })

                email_message = EmailMessage(
                    subject=subject,
                    body=html_message,
                    from_email=from_email,
                    to=to_email,
                )
                email_message.content_subtype = 'html'
                email_message.send()

            except:
                pass

            messages.success(request, 'Account created successfully!')
            return redirect('signIn')
    return render(request, 'admin/auth/sign-up.html')

# Log In/Sign In


def signIn(request):
    error_message = ''
    demo_mode = True if 'core.middleware.middleware.DemoModeMiddleware' in settings.MIDDLEWARE else False

    form = LoginForm()
    
    if not request.user.is_authenticated:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('login[password]')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if user.role == 'Admin' or user.role == 'Editor':
                    return redirect('admin_home')
                elif user.role == 'User':
                    return redirect('userDashboard')
                elif user.role == 'Manager':
                    return redirect('hrmManagerDashboard')
                elif user.role == 'HR':
                    return redirect('hrmHrDashboard')
                elif user.role == 'Employee':
                    return redirect('hrmEmployeeDashboard')

            else:
                error_message = 'Invalid username or password. Try again.'
        else:
            error_message = ''

        return render(request, 'admin/auth/login.html', {'error_message': error_message, 'demo_mode': demo_mode, 'form': form})
    else:
        if request.user.role == 'Admin' or request.user.role == 'Editor':
            return redirect('admin_home')
        elif request.user.role == 'User':
            return redirect('userDashboard')
        elif request.user.role == 'Manager':
            return redirect('hrmManagerDashboard')
        elif request.user.role == 'HR':
            return redirect('hrmHrDashboard')
        elif request.user.role == 'Employee':
            return redirect('hrmEmployeeDashboard')

# Log Out


@login_required(login_url='signIn')
def logout_view(request):
    logout(request)
    # Redirect the user to a success page or another appropriate page
    return redirect('signIn')

# # # # # # # # # # # # # # # # # #
    # Reset Password #
# # # # # # # # # # # # # # # # # #


def initiate_password_reset(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        try:
            user = User.objects.get(username=username)
            generate_reset_token_and_send_email(user, request)

            return redirect('initiate_password_reset')
        except User.DoesNotExist:
            messages.warning(request, 'Invalid username!')
            return redirect('initiate_password_reset')
    context = {
        'title': 'Forgot Password'
    }
    return render(request, 'admin/auth/forget-password.html', context)


def reset_password(request, token):
    try:
        password_reset_token = PasswordResetToken.objects.get(token=token)
        if password_reset_token.is_expired():
            messages.warning(
                request, 'The password reset time has expired. Try again.')
            return redirect('password_reset')

        if request.method == 'POST':
            new_password1 = request.POST.get('new_password1')
            new_password2 = request.POST.get('new_password2')
            if new_password1 == new_password2:

                user = password_reset_token.user
                user.set_password(new_password1)
                user.save()

                update_session_auth_hash(request, user)

                password_reset_token.delete()
                messages.success(request, 'Password reset successfully!')
                return redirect('signIn')
            else:
                messages.warning(
                    request, 'Something went wrong. Please try again.')
                return redirect('reset_password', token=token)
        context = {
            'title': 'Reset Password'
        }
        return render(request, 'admin/auth/reset.html', context)
    except PasswordResetToken.DoesNotExist:
        messages.warning(
            request, 'Invalid token. Please ensure you have the correct link.')
        return redirect('initiate_password_reset')
    except Exception as e:
        messages.warning(request, f'An error occurred: {str(e)}')
        return redirect('initiate_password_reset')


def error_404(request, exception):
    return render(request, 'error/error_404.html', status=404)