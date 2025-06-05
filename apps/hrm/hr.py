from django.shortcuts import render, redirect, get_object_or_404
from apps.hrm.models import *
from apps.crm.models import *
from apps.hrm.forms import *
from django.http import Http404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from core.decorators import admin_manager_role_required, hr_role_required, not_terminated
from apps.authapp.models import *
from apps.settings.models import *
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string

# ====================HRM Hrs====================


@login_required(login_url='signIn')
@not_terminated
def hrmHrList(request):
    if request.user.role == 'Admin':
        hrs = Hr.objects.all()
        branches = Branch.objects.all()
    else:
        hrs = Hr.objects.filter(userprofile__branch=request.user.userprofile.branch)
        branches = Branch.objects.filter(id=request.user.userprofile.branch.id)

    if request.method == 'POST':
        if 'create_hr' in request.POST:
            username = request.POST.get('username')
            name = request.POST.get('name')
            email = request.POST.get('email')
            password = request.POST.get('password')

            branch_pk = request.POST.get('branch')
            branch = get_object_or_404(Branch, id=branch_pk)

            department_pk = request.POST.get('department')
            department = get_object_or_404(Department, id=department_pk)

            designation_pk = request.POST.get('designation')
            designation = get_object_or_404(Designation, id=designation_pk)

            job_type_pk = request.POST.get('job_type')
            job_type = get_object_or_404(JobType, id=job_type_pk)

            if Hr.objects.filter(username__iexact=username):
                messages.warning(request, 'Username already exists')
                return redirect('hrmHrList')

            if Hr.objects.filter(email__iexact=email):
                messages.warning(request, 'Email already exists')
                return redirect('hrmHrList')

            user = Hr.objects.create_user(
                username=username, email=email, password=password)

            if user:
                user.userprofile.name = name
                user.userprofile.branch = branch
                user.userprofile.department = department
                user.userprofile.designation = designation
                user.userprofile.job_type = job_type
                user.userprofile.save()

                Payroll.objects.create(employee=user)
                
                try:
                    # Send a welcome email to the hr
                    website_settings = websiteSetting.objects.first()
                    header_footer = HeaderFooter.objects.first()
                    subject = f'Welcome to {website_settings.name}'
                    from_email = f'"{website_settings.name}" <{settings.DEFAULT_FROM_EMAIL}>'
                    to_email = [email]

                    # Load the HTML email template
                    html_message = render_to_string('admin/auth/email/welcome.html', {
                        'username': username,
                        'settings': website_settings,
                        'footer': header_footer,
                    })

                    email_message = EmailMessage(
                        subject=subject,
                        body=html_message,
                        from_email=from_email,
                        to=to_email,
                    )
                    email_message.content_subtype = 'html'
                    email_message.send()

                    messages.success(request, 'Hr created successfully!')
                except Exception as e:
                    messages.warning(request, 'Hr created successfully!')

                return redirect('hrmHrEdit', user.userprofile.slug)

    context = {
        'title': 'Hrs',
        'form': bDDJform(),
        'hrs': hrs,
        'branches': branches,
    }
    if request.user.role == 'Admin':
        return render(request, 'hrm/admin/main/hr/list.html', context)
    elif request.user.role == 'Manager':
        return render(request, 'hrm/manager/main/hr/list.html', context)
    else:
        return redirect('signIn')

# Hr profile edit (Admin)


@login_required(login_url='signIn')
@not_terminated
def hrmHrEdit(request, slug):
    if request.user.role == 'Admin':
        branches = Branch.objects.all()
    else:
        branches = Branch.objects.filter(id=request.user.userprofile.branch.id)
    try:
        profile = get_object_or_404(UserProfile, slug=slug)
        hr = profile.user
    except UserProfile.DoesNotExist:
        raise Http404("User profile does not exist")

    if request.method == 'POST':
        form = StaffProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(
                request, f'Hr [{hr}] profile updated successfully!')
            return redirect('hrmHrEdit', slug=hr.userprofile.slug)
    else:
        form = StaffProfileForm(instance=profile)

    context = {
        'title': 'Edit',
        'form': form,
        'profile': profile,
        'hr': hr,
        'branches': branches,
    }
    if request.user.role == 'Admin':
        return render(request, 'hrm/admin/main/hr/edit.html', context)
    elif request.user.role == 'Manager':
        return render(request, 'hrm/manager/main/hr/edit.html', context)
    else:
        return redirect('signIn')

# Hr profile delete (Admin)


@login_required(login_url='signIn')
@admin_manager_role_required
@not_terminated
def hrmHrDelete(request, slug):
    profile = get_object_or_404(UserProfile, slug=slug)
    hr = profile.user
    hr.delete()
    messages.warning(request, 'Hr deleted successfully!')
    return redirect('hrmHrList')

# ================ HR Dashboard ================#


@login_required(login_url='signIn')
@hr_role_required
@not_terminated
def hrmHrDashboard(request):
    employees = UserProfile.objects.filter(
        branch=request.user.userprofile.branch)

    branch = Branch.objects.all()

    projects = crmProjects.objects.filter(team__in=[request.user])

    meetings = Meeting.objects.filter(branch=request.user.userprofile.branch).order_by(
        '-meeting_date', '-meeting_time')

    notices = Notice.objects.filter(
        branch=request.user.userprofile.branch).order_by('-start_date')

    holidays = Holiday.objects.filter(branch=request.user.userprofile.branch).order_by('-start_date')

    leaves = Leave.objects.filter(
        employee=request.user).order_by('-start_date')

    events = Event.objects.filter(
        branch=request.user.userprofile.branch, is_active=True)

    context = {
        'title': 'Dashboard',
        'employees': employees,
        'branch': branch,
        'projects': projects,
        'meetings': meetings,
        'notices': notices,
        'holidays': holidays,
        'leaves': leaves,
        'events': events,
    }
    return render(request, 'hrm/hr/main/index.html', context)

# ================  ================#
