from django.shortcuts import render, redirect, get_object_or_404
from apps.hrm.models import *
from apps.crm.models import *
from apps.hrm.forms import *
from django.http import Http404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from core.decorators import not_terminated, admin_manager_hr_role_required, employee_role_required
from apps.authapp.models import *
from apps.settings.models import *
from django.core.mail import EmailMessage
from django.conf import settings
from datetime import timedelta
from django.template.loader import render_to_string
from apps.hrm.views import calculate_net_salary

# ====================HRM Employees====================
@login_required(login_url='signIn')
@not_terminated
def hrmEmployeeList(request):
    if request.user.role == 'Admin':
        employees = Employee.objects.all()
        branches = Branch.objects.all()
    else:
        employees = Employee.objects.filter(userprofile__branch=request.user.userprofile.branch)
        branches = Branch.objects.filter(id=request.user.userprofile.branch.id)
    
    if request.method == 'POST':
        if 'create_employee' in request.POST:
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
            
            if Employee.objects.filter(username__iexact=username):
                messages.warning(request, 'Username already exists')
                return redirect('hrmEmployeeList')
            
            if Employee.objects.filter(email__iexact=email):
                messages.warning(request, 'Email already exists')
                return redirect('hrmEmployeeList')
            
            user = Employee.objects.create_user(username=username, email=email, password=password)
            
            if user:
                user.userprofile.name = name 
                user.userprofile.branch = branch
                user.userprofile.department = department
                user.userprofile.designation = designation
                user.userprofile.job_type = job_type
                user.userprofile.save()
                
                Payroll.objects.create(employee=user)
                
                try:
                    # Send a welcome email to the employee
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
                    
                    messages.success(request, 'Employee created successfully!')
                except Exception as e:
                    messages.warning(request, 'Employee created successfully! But email not sent. Configure SMTP in .env')
                
                return redirect('hrmEmployeeEdit', user.userprofile.slug)

    context = {
        'title': 'Employees',
        'form' : bDDJform(),
        'employees': employees,
        'branches' : branches,
    }
    if request.user.role == 'Admin':
        return render(request, 'hrm/admin/main/employee/list.html', context)
    elif request.user.role == 'Manager':
        return render(request, 'hrm/manager/main/employee/list.html', context)
    elif request.user.role == 'HR':
        return render(request, 'hrm/hr/main/employee/list.html', context)
    else:
        return redirect('signIn')

# Employee profile edit (Admin)
@login_required(login_url='signIn')
@not_terminated
def hrmEmployeeEdit(request, slug):
    if request.user.role == 'Admin':
        branches = Branch.objects.all()
    else:
        branches = Branch.objects.filter(id=request.user.userprofile.branch.id)
    try:
        profile = get_object_or_404(UserProfile, slug=slug)
        employee = profile.user
    except UserProfile.DoesNotExist:
        raise Http404("User profile does not exist")

    if request.method == 'POST':
        form = StaffProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            employee.email = email
            employee.save()
            form.save()
            messages.success(request, f'Employee [{employee}] profile updated successfully!')
            return redirect('hrmEmployeeEdit', slug=employee.userprofile.slug)
    else:
        form = StaffProfileForm(instance=profile)

    context = {
        'title': 'Edit',
        'form': form,
        'profile': profile,
        'employee': employee,
        'branches': branches,
    }
    if request.user.role == 'Admin':
        return render(request, 'hrm/admin/main/employee/edit.html', context)
    elif request.user.role == 'Manager':
        return render(request, 'hrm/manager/main/employee/edit.html', context)
    elif request.user.role == 'HR':
        return render(request, 'hrm/hr/main/employee/edit.html', context)
    else:
        return redirect('signIn')

# Employee profile delete (Admin)
@login_required(login_url='signIn')
@admin_manager_hr_role_required
@not_terminated
def hrmEmployeeDelete(request, slug):
    profile = get_object_or_404(UserProfile, slug=slug)
    employee = profile.user
    employee.delete()
    messages.warning(request, 'Employee deleted successfully!')
    return redirect('hrmEmployeeList')

#============== HRM Employee Dashboard ==============#
@login_required(login_url='signIn')
@employee_role_required
@not_terminated
def hrmEmployeeDashboard(request):
    colleagues = UserProfile.objects.filter(
        branch=request.user.userprofile.branch, department=request.user.userprofile.department).exclude(user=request.user)

    branch = Branch.objects.filter(
        id=request.user.userprofile.branch.id)

    projects = crmProjects.objects.filter(
        team__in=[request.user])

    meetings = Meeting.objects.filter(
        branch=request.user.userprofile.branch, department=request.user.userprofile.department).order_by('-meeting_date', '-meeting_time')

    notices = Notice.objects.filter(
        branch=request.user.userprofile.branch, department=request.user.userprofile.department).order_by('-start_date')

    holidays = Holiday.objects.filter(
        branch=request.user.userprofile.branch).order_by('-start_date')

    leaves = Leave.objects.filter(
        employee=request.user).order_by('-start_date')

    events = Event.objects.filter(
        branch=request.user.userprofile.branch, is_active=True)
    
    context = {
        'title': 'Dashboard',
        'colleagues': colleagues,
        'branch': branch,
        'projects': projects,
        'meetings': meetings,
        'notices': notices,
        'holidays': holidays,
        'leaves': leaves,
        'events': events,
    }
    
    return render(request, 'hrm/employee/main/index.html', context)

#============== Employee Payroll ==============#
@login_required(login_url='signIn')
@employee_role_required
@not_terminated
def hrmEmployeePayroll(request):
    payroll = Payroll.objects.get(employee=request.user)
    
    allowances = Allowance.objects.filter(payroll=payroll)
    deductions = Deduction.objects.filter(payroll=payroll)
    salary = BasicSalary.objects.filter(payroll=payroll).first()
    
    payroll.salary = salary
    payroll.allowances = allowances
    payroll.deductions = deductions
    
    total_allowance = sum(allowance.amount for allowance in allowances) or 0.0
    total_deduction = sum(deduction.amount for deduction in deductions) or 0.0
    
    if salary:
        payroll.net_salary = salary.amount + total_allowance - total_deduction
    else:
        payroll.net_salary = 0.0
        
    context = {
        'title': 'Payroll',
        'payroll': payroll,
    }
    return render(request, 'hrm/employee/main/payroll.html', context)

#============== Employee Salary Details ==============#
@login_required(login_url='signIn')
@employee_role_required
@not_terminated
def hrmEmployeeSalaryDetails(request):
    payroll = Payroll.objects.get(employee=request.user)
    
    allowances = Allowance.objects.filter(payroll=payroll)
    deductions = Deduction.objects.filter(payroll=payroll)
    salary = BasicSalary.objects.filter(payroll=payroll).first()
    
    payroll.salary = salary
    payroll.allowances = allowances
    payroll.deductions = deductions
    
    total_allowance = sum(allowance.amount for allowance in allowances) or 0.0
    total_deduction = sum(deduction.amount for deduction in deductions) or 0.0
    
    # Calculate net salary
    if isinstance(salary, BasicSalary):
        net_salary = salary.amount + total_allowance - total_deduction
    else:
        net_salary = 0.0
        
    context = {
        'title': 'Salary Details',
        'payroll': payroll,
        
        'allowances': allowances,
        'deductions': deductions,
        'salary': salary,
        
        'total_allowance': total_allowance,
        'total_deduction': total_deduction,
        'total_salary': salary,
        'net_salary': net_salary,
    }
    return render(request, 'hrm/employee/main/payroll/details.html', context)

#============ Employee Payslips =============#
@login_required(login_url='signIn')
@employee_role_required
@not_terminated
def hrmEmployeePayslips(request):
    payroll = Payroll.objects.get(employee=request.user)
    payslips = Payslip.objects.filter(payroll=payroll).order_by('-created_at')
    
    context = {
        'title': 'Payslips',
        'payslips': payslips,
    }
    return render(request, 'hrm/employee/main/payslips.html', context)

#=========== Employee Projects ============#
@login_required(login_url='signIn')
@employee_role_required
@not_terminated
def hrmEmployeeProjects(request):
    projects = crmProjects.objects.filter(team__in=[request.user])
    
    context = {
        'title': 'Projects',
        'projects': projects,
    }
    return render(request, 'hrm/employee/main/projects/projects.html', context)

#========== Employee Project Task =========#
@login_required(login_url='signIn')
@employee_role_required
@not_terminated
def hrmEmployeeProjectTask(request, slug):
    project = crmProjects.objects.get(slug=slug)
    tasks = crmTasks.objects.filter(project=project, assigned_to__in=[request.user])
    
    context = {
        'title': 'Tasks',
        'project': project,
        'tasks': tasks,
    }
    return render(request, 'hrm/employee/main/projects/tasks.html', context)