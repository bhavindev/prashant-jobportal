from django.shortcuts import render, get_object_or_404, redirect
from core.decorators import admin_role_required, admin_manager_hr_role_required, not_terminated
from django.contrib.auth.decorators import login_required
from apps.authapp.models import User
from apps.hrm.models import *
from apps.crm.models import *
from django.views import generic
from django.utils.safestring import mark_safe
from datetime import timedelta, datetime, date
import calendar
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from apps.hrm.forms import *
from apps.settings.models import websiteSetting, HeaderFooter
from django.core.mail import EmailMessage
from django.conf import settings
from django.utils import timezone
from django.utils.timezone import localtime
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string

# ============== HRM Dashboard ==============#


@login_required(login_url='signIn')
@admin_role_required
def hrmDashboard(request):

    employees = User.objects.filter(role='Employee')
    managers = User.objects.filter(role='Manager')
    hrs = User.objects.filter(role='HR')
    total_staff = employees.count() + managers.count() + hrs.count() or 0

    branches = Branch.objects.all()
    total_branches = branches.count() or 0

    departments = Department.objects.all()
    total_departments = departments.count() or 0

    prjects = crmProjects.objects.all()
    total_projects = prjects.count() or 0

    meetings = Meeting.objects.all().order_by('-meeting_date', '-meeting_time')

    events = Event.objects.get_all_events()

    notices = Notice.objects.all().order_by('-start_date')

    holidays = Holiday.objects.all().order_by('-start_date')

    leaves = Leave.objects.all().order_by('-start_date')

    context = {
        'title': 'HRM',

        'employees': employees,
        'managers': managers,
        'hrs': hrs,
        'total_staff': total_staff,

        'branches': branches,
        'total_branches': total_branches,

        'departments': departments,
        'total_departments': total_departments,

        'prjects': prjects,
        'total_projects': total_projects,

        'meetings': meetings,
        'events': events,
        'notices': notices,
        'holidays': holidays,
        'leaves': leaves,
    }

    return render(request, 'hrm/admin/main/index.html', context)

# ============== Admin Event Calendar ==============#
# ======= Get Date =========#


def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split("-"))
        return date(year, month, day=1)
    return datetime.today()

# ======= Previous Month =========#


def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = "month=" + str(prev_month.year) + "-" + str(prev_month.month)
    return month

# ======= Next Month =========#


def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = "month=" + str(next_month.year) + "-" + str(next_month.month)
    return month

# ======= Canlenar View =======#


class CalendarViewNew(LoginRequiredMixin, generic.View):
    login_url = reverse_lazy('signIn')
    form_class = EventForm
    template_paths = {
        'Admin': 'hrm/admin/main/event/calendar.html',
        'Manager': 'hrm/manager/main/event/calendar.html',
        'HR': 'hrm/hr/main/event/calendar.html',
        'Employee': 'hrm/employee/main/event/calendar.html'
    }

    def get(self, request, *args, **kwargs):
        forms = self.form_class()

        if request.user.role == 'Admin':
            branches = Branch.objects.all()
            events = Event.objects.get_all_events()
            events_month = Event.objects.get_running_events()
        else:
            branches = Branch.objects.filter(
                id=request.user.userprofile.branch.id)
            print('Brnach Are: ', branches)
            events = Event.objects.filter(
                branch=request.user.userprofile.branch, is_active=True)
            events_month = Event.objects.filter(
                branch=request.user.userprofile.branch, is_active=True, end_time__gte=datetime.now().date(),).order_by("start_time")

        event_list = []

        for event in events:
            event_list.append({
                "id": event.id,
                "title": event.title,
                "start": event.start_time.strftime("%Y-%m-%d"),
                "end": event.end_time.strftime("%Y-%m-%d"),
                "description": event.description,
                "branch": event.branch.name if event.branch else None,
                "created_by": event.created_by.userprofile.name if event.created_by else None,
            })
        context = {
            'title': 'All Events',
            "form": forms,
            "events": event_list,
            "events_month": events_month,
            'branches': branches,
        }

        template_name = self.template_paths.get(
            request.user.role, 'hrm/admin/main/holiday/index.html')

        return render(request, template_name, context)

    def post(self, request, *args, **kwargs):
        forms = self.form_class(request.POST)
        if forms.is_valid():
            form = forms.save(commit=False)
            form.created_by = request.user
            form.save()
            messages.success(request, 'Event Created Successfully.')
            return redirect("calendar")

        context = {"form": forms}

        template_name = self.template_paths.get(
            request.user.role, 'hrm/admin/main/holiday/index.html')

        return render(request, template_name, context)

# ====== Event Delete View ======#


def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        event.delete()
        return JsonResponse({'message': 'Event deleted successfully.'})
    else:
        return JsonResponse({'message': 'Error!'}, status=400)

# ====== Event Next Week View ======#


def next_week(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        next_event = Event(
            title=event.title,
            description=event.description,
            start_time=event.start_time + timedelta(days=7),
            end_time=event.end_time + timedelta(days=7),
            branch=event.branch or None,
            created_by=event.created_by
        )
        next_event.save()
        event.delete()
        return JsonResponse({'message': 'Event added to next week successfully!'})
    else:
        return JsonResponse({'message': 'Error!'}, status=400)

# ====== Event Next Day View ======#


def next_day(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        next_event = Event(
            title=event.title,
            description=event.description,
            start_time=event.start_time + timedelta(days=1),
            end_time=event.end_time + timedelta(days=1),
            branch=event.branch or None,
            created_by=event.created_by
        )
        next_event.save()
        event.delete()
        return JsonResponse({'message': 'Event added to next day successfully!'})
    else:
        return JsonResponse({'message': 'Error!'}, status=400)

# ============== Admin Payroll View ==============#

@login_required(login_url='signIn')
def hrmPayroll(request):
    if request.user.role == 'Admin':
        payrolls = Payroll.objects.all().order_by('-created_at')
        employees = User.objects.filter()
    else:
        payrolls = Payroll.objects.filter(
            employee__userprofile__branch=request.user.userprofile.branch).exclude(pk=request.user.pk).order_by('-created_at')
        employees = User.objects.filter(
            userprofile__branch=request.user.userprofile.branch).exclude(pk=request.user.pk)
    
    for payroll in payrolls:
        allowances = Allowance.objects.filter(payroll=payroll)
        deductions = Deduction.objects.filter(payroll=payroll)
        salary = BasicSalary.objects.filter(payroll=payroll).first()
        payroll.salary = salary

        total_allowance = sum(allowance.amount for allowance in allowances) or 0.0
        total_deduction = sum(deduction.amount for deduction in deductions) or 0.0

        if salary:
            payroll.net_salary = salary.amount + total_allowance - total_deduction
        else:
            payroll.net_salary = 0.0

    if request.method == 'POST' and 'create_payroll' in request.POST:
        form = PayrollForm(request.POST)
        if form.is_valid():
            employee = form.cleaned_data['employee']
            existing_payroll = Payroll.objects.filter(employee=employee).exists()
            if existing_payroll:
                messages.warning(request, 'A payroll for this employee already exists.')
                return redirect('hrmPayroll')
            else:
                payroll_instance=form.save()
                messages.success(request, 'Payroll Created Successfully.')
                return redirect('hrmPayrollDetail' , id=payroll_instance.id)

    context = {
        'title': 'Payroll',
        'payrolls': payrolls,
        'employees': employees,
        'form': PayrollForm(),
    }

    if request.user.role == 'Admin':
        return render(request, 'hrm/admin/main/payroll/payroll.html', context)
    elif request.user.role == 'Manager':
        return render(request, 'hrm/manager/main/payroll/payroll.html', context)
    elif request.user.role == 'HR':
        return render(request, 'hrm/hr/main/payroll/payroll.html', context)
    else:
        return redirect('signIn')
    
# ============== Payroll Edit/Detail View ==============#
@login_required(login_url='signIn')
def hrmPayrollDetail(request, id):
    payroll = get_object_or_404(Payroll, id=id)
    
    allowances = Allowance.objects.filter(payroll=payroll)
    deductions = Deduction.objects.filter(payroll=payroll)
    salary = BasicSalary.objects.filter(payroll=payroll).first() or 0.0
    
    total_allowance = sum(allowance.amount for allowance in allowances) or 0.0
    total_deduction = sum(deduction.amount for deduction in deductions) or 0.0
    
    # Calculate net salary
    if isinstance(salary, BasicSalary):
        net_salary = salary.amount + total_allowance - total_deduction
    else:
        net_salary = 0.0
    
    if request.method == 'POST':
        if 'create_allowance' in request.POST:
            form = AllowanceForm(request.POST)
            if form.is_valid():
                allowance = form.save(commit=False)
                allowance.payroll = payroll
                allowance.save()
                messages.success(request, 'Allowance Added Successfully.')
                return redirect('hrmPayrollDetail', id=id)
        
        elif 'create_deduction' in request.POST:
            form = DeductionForm(request.POST)
            if form.is_valid():
                deduction = form.save(commit=False)
                deduction.payroll = payroll
                deduction.save()
                messages.success(request, 'Deduction Added Successfully.')
                return redirect('hrmPayrollDetail', id=id)
        
        elif 'create_salary' in request.POST:
            form = SalaryForm(request.POST)
            if form.is_valid():
                salary = form.save(commit=False)
                salary.payroll = payroll
                salary.save()
                messages.success(request, 'Salary Added Successfully.')
                return redirect('hrmPayrollDetail', id=id)

    context = {
        'title': 'Payroll',
        'payroll': payroll,
        
        'allowances': allowances,
        'deductions': deductions,
        'salary': salary,
        
        'total_allowance': total_allowance,
        'total_deduction': total_deduction,
        'total_salary': salary,
        'net_salary': net_salary,
    
    }
    if request.user.role == 'Admin':
        return render(request, 'hrm/admin/main/payroll/details.html', context)
    elif request.user.role == 'Manager':
        return render(request, 'hrm/manager/main/payroll/details.html', context)
    elif request.user.role == 'HR':
        return render(request, 'hrm/hr/main/payroll/details.html', context)
    else:
        return redirect('signIn')
    
@login_required(login_url='signIn')
def salaryEdit(request, id):
    salary = get_object_or_404(BasicSalary, id=id)
    if (request.user.role == 'Admin' or (request.user.role == 'Manager' and request.user.userprofile.branch == salary.payroll.employee.userprofile.branch) or (request.user.role == 'HR' and request.user.userprofile.branch == salary.payroll.employee.userprofile.branch)):
        if request.method == 'POST' and 'update_salary' in request.POST:
            form = SalaryForm(request.POST, instance=salary)
            if form.is_valid():
                form.save()
                messages.success(request, 'Salary Updated Successfully.')
                return redirect('hrmPayrollDetail', id=salary.payroll.id)
    else:
        return redirect('signIn')

@login_required(login_url='signIn')
def salaryDelete(request, id):
    salary = get_object_or_404(BasicSalary, id=id)
    if (request.user.role == 'Admin' or (request.user.role == 'Manager' and request.user.userprofile.branch == salary.payroll.employee.userprofile.branch) or (request.user.role == 'HR' and request.user.userprofile.branch == salary.payroll.employee.userprofile.branch)):
        salary.delete()
        messages.warning(request, 'Salary Deleted Successfully.')
        return redirect('hrmPayrollDetail', id=salary.payroll.id)
    else:
        return redirect('signIn')

@login_required(login_url='signIn')
def allowanceEdit(request, id):
    allowance = get_object_or_404(Allowance, id=id)
    if (request.user.role == 'Admin' or (request.user.role == 'Manager' and request.user.userprofile.branch == allowance.payroll.employee.userprofile.branch) or (request.user.role == 'HR' and request.user.userprofile.branch == allowance.payroll.employee.userprofile.branch)):
        if request.method == 'POST' and 'update_allowance' in request.POST:
            form = AllowanceForm(request.POST, instance=allowance)
            if form.is_valid():
                form.save()
                messages.success(request, 'Allowance Updated Successfully.')
                return redirect('hrmPayrollDetail', id=allowance.payroll.id)
    else:
        return redirect('signIn')
        
@login_required(login_url='signIn')
def allowanceDelete(request, id):
    allowance = get_object_or_404(Allowance, id=id)
    if (request.user.role == 'Admin' or (request.user.role == 'Manager' and request.user.userprofile.branch == allowance.payroll.employee.userprofile.branch) or (request.user.role == 'HR' and request.user.userprofile.branch == allowance.payroll.employee.userprofile.branch)):
        allowance.delete()
        messages.warning(request, 'Allowance Deleted Successfully.')
        return redirect('hrmPayrollDetail', id=allowance.payroll.id)
    else:
        return redirect('signIn')

@login_required(login_url='signIn')
def deductionEdit(request, id):
    deduction = get_object_or_404(Deduction, id=id)
    if (request.user.role == 'Admin' or (request.user.role == 'Manager' and request.user.userprofile.branch == deduction.payroll.employee.userprofile.branch) or (request.user.role == 'HR' and request.user.userprofile.branch == deduction.payroll.employee.userprofile.branch)):
        if request.method == 'POST' and 'update_deduction' in request.POST:
            form = DeductionForm(request.POST, instance=deduction)
            if form.is_valid():
                form.save()
                messages.success(request, 'Deduction Updated Successfully.')
                return redirect('hrmPayrollDetail', id=deduction.payroll.id)
    else:
        return redirect('signIn')

@login_required(login_url='signIn')
def deductionDelete(request, id):
    deduction = get_object_or_404(Deduction, id=id)
    if (request.user.role == 'Admin' or (request.user.role == 'Manager' and request.user.userprofile.branch == deduction.payroll.employee.userprofile.branch) or (request.user.role == 'HR' and request.user.userprofile.branch == deduction.payroll.employee.userprofile.branch)):
        deduction.delete()
        messages.warning(request, 'Deduction Deleted Successfully.')
        return redirect('hrmPayrollDetail', id=deduction.payroll.id)
    else:
        return redirect('signIn')

@login_required(login_url='signIn')
def hrmPayrollDelete(request, id):
    payroll = get_object_or_404(Payroll, id=id)
    if (request.user.role == 'Admin' or (request.user.role == 'Manager' and request.user.userprofile.branch == payroll.employee.userprofile.branch) or (request.user.role == 'HR' and request.user.userprofile.branch == payroll.employee.userprofile.branch)):
        payroll.delete()
        messages.warning(request, 'Payroll Deleted Successfully.')
        return redirect('hrmPayroll')
    else:
        return redirect('signIn')

# ============== Generate Payslip ==============#
def generatePayslip():
    today = timezone.now()
    current_month = today.month
    current_year = today.year
    payrolls = Payroll.objects.all()
    
    # Iterate over all payrolls
    for payroll in payrolls:
        # Check if a payslip already exists for the current month and year for the payroll
        existing_payslip = Payslip.objects.filter(payroll=payroll, date__month=current_month, date__year=current_year).exists()
        
        # If a payslip does not exist, create one
        if not existing_payslip:
            basic_salary = BasicSalary.objects.filter(payroll=payroll).first()
            if basic_salary:
                salary_type = basic_salary.type

                if salary_type == 'Monthly':
                    first_day_of_month = today.replace(day=1)
                    Payslip.objects.create(payroll=payroll, status='Unpaid', date=first_day_of_month)
                elif salary_type == 'Yearly':
                    first_day_of_year = today.replace(month=1, day=1)
                    Payslip.objects.create(payroll=payroll, status='Unpaid', date=first_day_of_year)
                elif salary_type == 'Weekly':
                    first_day_of_week = today - timedelta(days=today.weekday())
                    Payslip.objects.create(payroll=payroll, status='Unpaid', date=first_day_of_week)
                elif salary_type == 'Bi-monthly':
                    if today.day <= 15:
                        first_day_of_month = today.replace(day=1)
                    else:
                        first_day_of_month = today.replace(day=16)
                    Payslip.objects.create(payroll=payroll, status='Unpaid', date=first_day_of_month)
                elif salary_type in ['Daily', 'Hourly', 'Commission-based', 'Contract-based', 'Retainer-based', 'Profit-sharing']:
                    Payslip.objects.create(payroll=payroll, status='Unpaid', date=today)



# ============== Admin Payslip View ==============#

def calculate_net_salary(payslips):
    for payslip in payslips:
        payroll = payslip.payroll
        allowances = Allowance.objects.filter(payroll=payroll)
        deductions = Deduction.objects.filter(payroll=payroll)
        salary = BasicSalary.objects.filter(payroll=payroll).first()

        total_allowance = sum(allowance.amount for allowance in allowances) or 0.0
        total_deduction = sum(deduction.amount for deduction in deductions) or 0.0

        if salary:
            payslip.salary = salary
            payslip.allowances = allowances
            payslip.deductions = deductions
            payslip.net_salary = salary.amount + total_allowance - total_deduction
        else:
            payslip.salary = 'Null'
            payslip.allowances = None
            payslip.deductions = None
            payslip.net_salary = 0.0
            
@login_required(login_url='signIn')    
def hrmPayslip(request):
    
    generatePayslip()

    if 'filtered_month' not in request.session or 'filtered_year' not in request.session:
        request.session['filtered_month'] = timezone.now().month
        request.session['filtered_year'] = timezone.now().year

    current_month = request.session['filtered_month']
    current_year = request.session['filtered_year']
    year_values = list(range(2020, 2041))

    if request.user.role == 'Admin':
        payslips = Payslip.objects.filter(date__month=current_month, date__year=current_year)
    elif request.user.role == 'Employee':
        payslips = Payslip.objects.filter(payroll__employee=request.user, date__month=current_month, date__year=current_year).order_by('-date')
    else:
        payslips = Payslip.objects.filter(payroll__employee__userprofile__branch=request.user.userprofile.branch, date__month=current_month, date__year=current_year)
    
    calculate_net_salary(payslips)
        
    
    if request.method == 'POST':
        if 'filter_payslip' in request.POST:
            month = int(request.POST.get('month'))
            year = int(request.POST.get('year'))
            if request.user.role == 'Admin':
                payslips = Payslip.objects.filter(date__month=month, date__year=year)
            elif request.user.role == 'Employee':
                payslips = Payslip.objects.filter(payroll__employee=request.user, date__month=month, date__year=year)
            else:
                payslips = Payslip.objects.filter(payroll__employee__userprofile__branch=request.user.userprofile.branch, date__month=month, date__year=year)
            
            request.session['filtered_month'] = month
            request.session['filtered_year'] = year
            
            calculate_net_salary(payslips)
            
            current_year = year
            current_month = month
            
            return redirect('hrmPayslip')
    
    request.session['filtered_month_expiry'] = (timezone.now() + timedelta(hours=1)).strftime('%Y-%m-%d')
    request.session['filtered_year_expiry'] = (timezone.now() + timedelta(hours=1)).strftime('%Y-%m-%d')
    
    context = {
        'title' : 'Payslips',
        'payslips' : payslips,
        'current_month' : current_month,
        'current_year' : current_year,
        'year_values' : year_values,
    }
    
    if request.user.role == 'Admin':
        return render(request, 'hrm/admin/main/payroll/payslips.html', context)
    elif request.user.role == 'Manager':
        return render(request, 'hrm/manager/main/payroll/payslips.html', context)
    elif request.user.role == 'HR':
        return render(request, 'hrm/hr/main/payroll/payslips.html', context)
    elif request.user.role == 'Employee':
        return render(request, 'hrm/employee/main/payroll/payslips.html', context)
    else:
        return redirect('signIn')

@login_required(login_url='signIn')
def hrmPayslipDetail(request, id):
    payslip = get_object_or_404(Payslip, id=id)
    
    if (request.user.role == 'Admin' or (request.user.role == 'Manager' and request.user.userprofile.branch == payslip.payroll.employee.userprofile.branch) or (request.user.role == 'HR' and request.user.userprofile.branch == payslip.payroll.employee.userprofile.branch) or payslip.payroll.employee == request.user):
        
        allowances = Allowance.objects.filter(payroll=payslip.payroll)
        deductions = Deduction.objects.filter(payroll=payslip.payroll)
        salary = BasicSalary.objects.filter(payroll=payslip.payroll).first()
        
        total_allowance = sum(allowance.amount for allowance in allowances) or 0.0
        total_deduction = sum(deduction.amount for deduction in deductions) or 0.0
        
        if salary:
            payslip.salary = salary
            payslip.allowances = allowances
            payslip.deductions = deductions
            payslip.net_salary = salary.amount + total_allowance - total_deduction
        else:
            payslip.salary = 'Null'
            payslip.allowances = None
            payslip.deductions = None
            payslip.net_salary = 0.0
        
        context = {
            'title' : f"{payslip.payroll.employee.userprofile.name}'s Payslip - {payslip.date.strftime('%B, %Y')}",
            'payslip' : payslip,
            'allowances' : allowances,
            'deductions' : deductions,
            'salary' : salary,
            'total_allowance' : total_allowance,
            'total_deduction' : total_deduction,
        }
        
        if request.user.role == 'Admin':
            return render(request, 'hrm/admin/main/payroll/slipdetails.html', context)
        elif request.user.role == 'Manager':
            return render(request, 'hrm/manager/main/payroll/slipdetails.html', context)
        elif request.user.role == 'HR':
            return render(request, 'hrm/hr/main/payroll/slipdetails.html', context)
        elif request.user.role == 'Employee':
            return render(request, 'hrm/employee/main/payroll/slipdetails.html', context)
        else:
            return redirect('signIn')
    else:
        return redirect('signIn')
    
def emailPyslip(request, id):
    payslip = get_object_or_404(Payslip, id=id)
    if request.method == 'POST' and 'email_payslip' in request.POST:
        try:
            website_settings = websiteSetting.objects.first()
            header_footer = HeaderFooter.objects.first()
            email = payslip.payroll.employee.email
            subject = f'Payslip for {payslip.date.strftime("%B, %Y")}'
            view_link = request.build_absolute_uri(reverse('hrmPayslipDetail', args=[str(payslip.id)]))
            from_email = f'"{website_settings.name}" <{settings.EMAIL_HOST_USER}>'
            recipient_list = [email, ]
            message_body = render_to_string('hrm/components/email/payslip.html', {
                'payslip': payslip,
                'view_link': view_link,
                'settings': website_settings,
                'footer': header_footer,
                })
            email = EmailMessage(
                subject=subject,
                body=message_body,
                from_email=from_email,
                to=recipient_list,
            )
            email.content_subtype = 'html'
            email.send()
            messages.success(request, 'Payslip sent successfully.')
        except Exception as e:
            messages.warning(request, e)
        return redirect('hrmPayslip')

def hrmPayslipMarkPaid(request, id):
    payslip = get_object_or_404(Payslip, id=id)
    salary = BasicSalary.objects.filter(payroll=payslip.payroll).first()
    if request.method == 'POST' and 'mark_paid' in request.POST:
        if salary:
            payslip.status = 'Paid'
            payslip.save()
            messages.success(request, 'Payslip Marked As Paid')
        else:
            messages.warning(request, 'Payslip has no salary!')
        return redirect('hrmPayslip')
    
# ============== Admin Branch View ==============#

@login_required(login_url='signIn')
@admin_role_required
@not_terminated
def hrmBranch(request):
    branches = Branch.objects.all()
    if request.method == 'POST' and 'create_branch' in request.POST:
        form = BranchForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Branch Created Successfully.')
            return redirect('hrmBranch')
    context = {
        'title': 'Branches',
        'branches': branches,
        'form': BranchForm(),
    }
    return render(request, 'hrm/admin/main/branch/index.html', context)

@login_required(login_url='signIn')
@admin_role_required
@not_terminated
def hrmBranchEdit(request, id):
    branch = get_object_or_404(Branch, id=id)
    if request.method == 'POST':
        form = BranchForm(request.POST, instance=branch)
        if form.is_valid():
            form.save()
            messages.success(request, 'Branch Updated Successfully.')
            return redirect('hrmBranch')

@login_required(login_url='signIn')
@admin_role_required
@not_terminated
def hrmBranchDelete(request, id):
    branch = get_object_or_404(Branch, id=id)
    branch.delete()
    messages.warning(request, 'Branch Deleted Successfully.')
    return redirect('hrmBranch')

# ============== Admin Department View ==============#

@login_required(login_url='signIn')
@admin_role_required
@not_terminated
def hrmDepartment(request):
    departments = Department.objects.all()
    if request.method == 'POST' and 'create_department' in request.POST:
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Department Created Successfully.')
            return redirect('hrmDepartment')
    context = {
        'title': 'Departments',
        'departments': departments,
        'form': DepartmentForm(),
    }
    return render(request, 'hrm/admin/main/department/index.html', context)

@login_required(login_url='signIn')
@admin_role_required
@not_terminated
def hrmDepartmentEdit(request, id):
    department = get_object_or_404(Department, id=id)
    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            messages.success(request, 'Department Updated Successfully.')
            return redirect('hrmDepartment')

@login_required(login_url='signIn')
@admin_role_required
@not_terminated
def hrmDepartmentDelete(request, id):
    department = get_object_or_404(Department, id=id)
    department.delete()
    messages.warning(request, 'Department Deleted Successfully.')
    return redirect('hrmDepartment')

# ============== Admin Designation View ==============#

@login_required(login_url='signIn')
@admin_role_required
@not_terminated
def hrmDesignation(request):
    designations = Designation.objects.all()
    if request.method == 'POST' and 'create_designation' in request.POST:
        form = DesignationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Designation Created Successfully.')
            return redirect('hrmDesignation')
    context = {
        'title': 'Designations',
        'designations': designations,
        'form': DesignationForm(),
    }
    return render(request, 'hrm/admin/main/designation/index.html', context)

@login_required(login_url='signIn')
@admin_role_required
@not_terminated
def hrmDesignationEdit(request, id):
    designation = get_object_or_404(Designation, id=id)
    if request.method == 'POST':
        form = DesignationForm(request.POST, instance=designation)
        if form.is_valid():
            form.save()
            messages.success(request, 'Designation Updated Successfully.')
            return redirect('hrmDesignation')

@login_required(login_url='signIn')
@admin_role_required
@not_terminated
def hrmDesignationDelete(request, id):
    designation = get_object_or_404(Designation, id=id)
    designation.delete()
    messages.warning(request, 'Designation Deleted Successfully.')
    return redirect('hrmDesignation')

# ============== Admin Job Type View ==============#

@login_required(login_url='signIn')
@admin_role_required
@not_terminated
def hrmJobType(request):
    job_types = JobType.objects.all()
    if request.method == 'POST' and 'create_job_type' in request.POST:
        form = JobTypeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Job Type Created Successfully.')
            return redirect('hrmJobType')
    context = {
        'title': 'Job Types',
        'job_types': job_types,
        'form': JobTypeForm(),
    }
    return render(request, 'hrm/admin/main/job_type/index.html', context)

@login_required(login_url='signIn')
@admin_role_required
@not_terminated
def hrmJobTypeEdit(request, id):
    job_type = get_object_or_404(JobType, id=id)
    if request.method == 'POST':
        form = JobTypeForm(request.POST, instance=job_type)
        if form.is_valid():
            form.save()
            messages.success(request, 'Job Type Updated Successfully.')
            return redirect('hrmJobType')

@login_required(login_url='signIn')
@admin_role_required
@not_terminated
def hrmJobTypeDelete(request, id):
    job_type = get_object_or_404(JobType, id=id)
    job_type.delete()
    messages.warning(request, 'Job Type Deleted Successfully.')
    return redirect('hrmJobType')

# ============== Admin Notice View ==============#
@login_required(login_url='signIn')
@not_terminated
def hrmNotices(request):
    if request.user.role == 'Admin':
        notices = Notice.objects.all().order_by('-start_date')
        branches = Branch.objects.all()
    else:
        notices = Notice.objects.filter(
            branch=request.user.userprofile.branch).order_by('-start_date')
        branches = Branch.objects.filter(id=request.user.userprofile.branch.id)

    departments = Department.objects.all()
    if request.method == 'POST' and 'create_notice' in request.POST:
        add_to_calendar = request.POST.get('add-to-calendar')
        form = NoticeForm(request.POST)
        if form.is_valid():
            notice = form.save(commit=False)
            notice.created_by = request.user
            notice.save()
            Notification.objects.create(
                title = f'{notice.title}',
                description = notice.description,
                branch = notice.branch,
                department = notice.department,
            )
            if add_to_calendar:
                event = Event.objects.create(
                    notice=notice,
                    title=form.cleaned_data['title'],
                    branch=form.cleaned_data['branch'],
                    description=form.cleaned_data['description'],
                    start_time=form.cleaned_data['start_date'],
                    end_time=form.cleaned_data['end_date'],
                    created_by=request.user
                )
                event.save()
            messages.success(request, 'Notice Created Successfully.')
            return redirect('hrmNotices')
    context = {
        'title': 'Notices',
        'notices': notices,
        'form': NoticeForm(),
        'bdform': bDDJform(),
        'branches': branches,
        'departments': departments,
    }
    if request.user.role == 'Admin':
        return render(request, 'hrm/admin/main/notice/index.html', context)
    elif request.user.role == 'Manager':
        return render(request, 'hrm/manager/main/notice/index.html', context)
    elif request.user.role == 'HR':
        return render(request, 'hrm/hr/main/notice/index.html', context)
    elif request.user.role == 'Employee':
        return render(request, 'hrm/employee/main/notice/index.html', context)
    else:
        return redirect('signIn')


@login_required(login_url='signIn')
@admin_manager_hr_role_required
@not_terminated
def hrmNoticeEdit(request, id):
    notice = get_object_or_404(Notice, id=id)

    if request.method == 'POST' and 'update_notice' in request.POST:
        branch_pk = request.POST.get('branch')
        department_pk = request.POST.get('department')

        branch = get_object_or_404(Branch, id=branch_pk)
        department = get_object_or_404(Department, id=department_pk)

        form = NoticeForm(request.POST, instance=notice)

        if form.is_valid():
            updated_notice = form.save(commit=False)
            updated_notice.branch = branch
            updated_notice.department = department
            updated_notice.created_by = request.user
            updated_notice.save()

            # Update Event
            try:
                event = get_object_or_404(Event, notice=notice)
                if event:
                    event.notice = updated_notice
                    event.title = form.cleaned_data['title']
                    event.branch = form.cleaned_data['branch']
                    event.description = form.cleaned_data['description']
                    event.start_time = form.cleaned_data['start_date']
                    event.end_time = form.cleaned_data['end_date']
                    event.created_by = request.user
                    event.save()
            except:
                pass

            messages.success(request, 'Notice Updated Successfully.')
            return redirect('hrmNotices')


@login_required(login_url='signIn')
@admin_manager_hr_role_required
@not_terminated
def hrmNoticeDelete(request, id):
    notice = get_object_or_404(Notice, id=id)

    try:
        event = get_object_or_404(Event, notice=notice)
        if event:
            event.delete()
    except:
        pass
    notice.delete()
    messages.warning(request, 'Notice Deleted Successfully.')
    return redirect('hrmNotices')

# ============== Admin Holiday View ==============#


@login_required(login_url='signIn')
@not_terminated
def hrmHolidays(request):
    if request.user.role == 'Admin':
        holidays = Holiday.objects.all().order_by('-start_date')
        branches = Branch.objects.all()
    else:
        holidays = Holiday.objects.filter(branch=request.user.userprofile.branch).order_by('-start_date')
        branches = Branch.objects.filter(id=request.user.userprofile.branch.id)

    if request.method == 'POST' and 'create_holiday' in request.POST:
        add_to_calendar = request.POST.get('add-to-calendar')
        form = HolidayForm(request.POST)
        if form.is_valid():
            holiday = form.save(commit=False)
            holiday.created_by = request.user
            holiday.save()
            Notification.objects.create(
                title = f'{holiday.occasion}',
                description = holiday.description,
                branch = holiday.branch,
            )
            if add_to_calendar:
                event = Event.objects.create(
                    holiday=holiday,
                    title=form.cleaned_data['occasion'],
                    branch=form.cleaned_data['branch'],
                    description=form.cleaned_data['description'],
                    start_time=form.cleaned_data['start_date'],
                    end_time=form.cleaned_data['end_date'],
                    created_by=request.user
                )
                event.save()
            messages.success(request, 'Holiday Created Successfully.')
            return redirect('hrmHolidays')
    context = {
        'title': 'Holidays',
        'holidays': holidays,
        'form': HolidayForm(),
        'branches': branches,
    }
    if request.user.role == 'Admin':
        return render(request, 'hrm/admin/main/holiday/index.html', context)
    elif request.user.role == 'Manager':
        return render(request, 'hrm/manager/main/holiday/index.html', context)
    elif request.user.role == 'HR':
        return render(request, 'hrm/hr/main/holiday/index.html', context)
    elif request.user.role == 'Employee':
        return render(request, 'hrm/employee/main/holiday/index.html', context)
    else:
        return redirect('signIn')


@login_required(login_url='signIn')
@admin_manager_hr_role_required
@not_terminated
def hrmHolidayEdit(request, id):
    holiday = get_object_or_404(Holiday, id=id)
    if request.method == 'POST' and 'update_holiday' in request.POST:
        branch_pk = request.POST.get('branch')
        branch = get_object_or_404(Branch, id=branch_pk)

        form = HolidayForm(request.POST, instance=holiday)
        if form.is_valid():
            updated_holiday = form.save(commit=False)
            updated_holiday.created_by = request.user
            updated_holiday.branch = branch
            updated_holiday.save()

            # Update Event
            try:
                event = get_object_or_404(Event, holiday=holiday)
                if event:
                    event.holiday = updated_holiday
                    event.title = form.cleaned_data['occasion']
                    event.branch = form.cleaned_data['branch']
                    event.description = form.cleaned_data['description']
                    event.start_time = form.cleaned_data['start_date']
                    event.end_time = form.cleaned_data['end_date']
                    event.created_by = request.user
                    event.save()
            except:
                pass

            messages.success(request, 'Holiday Updated Successfully.')
            return redirect('hrmHolidays')


@login_required(login_url='signIn')
@admin_manager_hr_role_required
@not_terminated
def hrmHolidayDelete(request, id):
    holiday = get_object_or_404(Holiday, id=id)
    try:
        event = get_object_or_404(Event, holiday=holiday)
        if event:
            event.delete()
    except:
        pass
    holiday.delete()
    messages.warning(request, 'Holiday Deleted Successfully.')
    return redirect('hrmHolidays')

# ============== Admin Leave Types View ==============#


@login_required(login_url='signIn')
@not_terminated
def hrmLeaveTypes(request):
    types = LeaveType.objects.all().order_by('-created_at')

    if request.method == 'POST' and 'create_type' in request.POST:
        form = LeaveTypeForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Leave type created successfully.')
            return redirect('hrmLeaveTypes')

    context = {
        'title': 'Leave Types',
        'types': types,
        'form': LeaveTypeForm()
    }

    if request.user.role == 'Admin':
        return render(request, 'hrm/admin/main/leave/partial/types.html', context)
    elif request.user.role == 'Manager':
        return render(request, 'hrm/manager/main/leave/partial/types.html', context)
    elif request.user.role == 'HR':
        return render(request, 'hrm/hr/main/leave/partial/types.html', context)
    else:
        return redirect('signIn')


@login_required(login_url='signIn')
@admin_manager_hr_role_required
@not_terminated
def hrmLeaveTypeEdit(request, id):
    type = get_object_or_404(LeaveType, id=id)

    if request.method == 'POST' and 'update_type' in request.POST:
        form = LeaveTypeForm(request.POST, instance=type)

        if form.is_valid():
            form.save()
            messages.success(request, 'Leave type updated successfully.')
            return redirect('hrmLeaveTypes')


@login_required(login_url='signIn')
@admin_manager_hr_role_required
@not_terminated
def hrmLeaveTypeDelete(request, id):
    type = get_object_or_404(LeaveType, id=id)
    type.delete()
    messages.warning(request, 'Leave type deleted successfully.')
    return redirect('hrmLeaveTypes')

# ============== Admin Leave View ==============#


@login_required(login_url='signIn')
@not_terminated
def hrmLeaves(request):
    if request.user.role == 'Admin':
        leaves = Leave.objects.all().order_by('-start_date')
        employees = User.objects.exclude(pk=request.user.pk)
        pending_requests = Leave.objects.filter(status='Pending').count()
        approved_requests = Leave.objects.filter(status='Approved').count()
        rejected_requests = Leave.objects.filter(status='Rejected').count()
        
    elif request.user.role == 'Employee':
        leaves = Leave.objects.filter(employee=request.user).order_by('-start_date')
        employees = ''
        pending_requests = Leave.objects.filter(status='Pending', employee=request.user).count()
        approved_requests = Leave.objects.filter(status='Approved', employee=request.user).count()
        rejected_requests = Leave.objects.filter(status='Rejected', employee=request.user).count()
    else:
        leaves = Leave.objects.filter(
            employee__userprofile__branch=request.user.userprofile.branch).order_by('-start_date')
        employees = User.objects.filter(
            userprofile__branch=request.user.userprofile.branch).exclude(pk=request.user.pk)
        pending_requests = Leave.objects.filter(
            status='Pending', employee__userprofile__branch=request.user.userprofile.branch).count()
        approved_requests = Leave.objects.filter(
            status='Approved', employee__userprofile__branch=request.user.userprofile.branch).count()
        rejected_requests = Leave.objects.filter(
            status='Rejected', employee__userprofile__branch=request.user.userprofile.branch).count()

    types = LeaveType.objects.all()

    if request.method == 'POST':
        if 'create_leave' in request.POST:
            form = LeaveForm(request.POST)
            if form.is_valid():
                leave = form.save(commit=False)
                leave.created_by = request.user
                leave.save()
                messages.success(request, 'Leave created successfully.')

        elif 'request_leave' in request.POST:
            request_form = LeaveRequestForm(request.POST)
            if request_form.is_valid():
                request_form = request_form.save(commit=False)
                request_form.employee = request.user
                request_form.status = 'Pending'
                request_form.created_by = request.user
                request_form.save()
                messages.success(request, 'Leave request sent successfully.')
                
        return redirect('hrmLeaves')

    context = {
        'title': 'Leaves',
        'leaves': leaves,
        'employees': employees,
        'types': types,
        'pending_requests': pending_requests,
        'approved_requests': approved_requests,
        'rejected_requests': rejected_requests,
        'form': LeaveForm(),
        'r_form': LeaveRequestForm()
    }

    template = 'hrm/admin/main/leave/index.html' if request.user.role == 'Admin' else \
               'hrm/manager/main/leave/index.html' if request.user.role == 'Manager' else \
               'hrm/hr/main/leave/index.html' if request.user.role == 'HR' else \
               'hrm/employee/main/leave/index.html' if request.user.role == 'Employee' else None

    if template:
        return render(request, template, context)
    else:
        return redirect('signIn')


@login_required(login_url='signIn')
@admin_manager_hr_role_required
@not_terminated
def hrmLeaveEdit(request, id):
    leave = get_object_or_404(Leave, id=id)

    if request.method == 'POST' and 'update_leave' in request.POST:
        form = LeaveForm(request.POST, instance=leave)

        if form.is_valid():
            updated_leave = form.save(commit=False)
            updated_leave.created_by = request.user
            updated_leave.save()
            messages.success(request, 'Leave updated successfully.')
            return redirect('hrmLeaves')


@login_required(login_url='signIn')
@admin_manager_hr_role_required
@not_terminated
def hrmLeaveMarkApproved(request, id):
    leave = get_object_or_404(Leave, id=id)
    if request.user.role == 'Admin' or request.user.role == 'HR' or request.user.role == 'Manager':
        leave.status = 'Approved'
        leave.created_by = request.user
        leave.save()
        messages.success(request, 'Leave request marked as approved.')
    else:
        messages.warning(request, 'Something went wrong.')
    return redirect('hrmLeaves')


@login_required(login_url='signIn')
@not_terminated
def hrmLeaveDelete(request, id):
    leave = get_object_or_404(Leave, id=id)
    if request.user.role == 'Admin' or request.user.role == 'HR' or request.user.role == 'Manager' or leave.employee == request.user:
        if leave.status == 'Pending':
            leave.delete()
            messages.warning(request, 'Leave deleted successfully.')
        else:
            messages.warning(request, 'Cannot delete an approved/rejected leave.')
    else:
        messages.warning(request, 'Something went wrong.')
    return redirect('hrmLeaves')

# ============== Admin Meeting View ==============#


@login_required(login_url='signIn')
@not_terminated
def hrmMeetings(request):
    if request.user.role == 'Admin':
        meetings = Meeting.objects.all().order_by('-meeting_date', '-meeting_time')
        branches = Branch.objects.all()
    else:
        meetings = Meeting.objects.filter(branch=request.user.userprofile.branch).order_by(
            '-meeting_date', '-meeting_time')
        branches = Branch.objects.filter(id=request.user.userprofile.branch.id)

    departments = Department.objects.all()
    if request.method == 'POST' and 'create_meeting' in request.POST:
        add_to_calendar = request.POST.get('add-to-calendar')
        form = MeetingForm(request.POST)
        if form.is_valid():
            meeting = form.save(commit=False)
            meeting.created_by = request.user
            meeting.save()
            
            Notification.objects.create(
                title = f'{meeting.title}',
                description = meeting.description,
                branch = meeting.branch,
                department = meeting.department,
            )

            if add_to_calendar:
                event = Event.objects.create(
                    meeting=meeting,
                    title=form.cleaned_data['title'],
                    branch=form.cleaned_data['branch'],
                    description=form.cleaned_data['description'],
                    start_time=form.cleaned_data['meeting_date'],
                    end_time=form.cleaned_data['meeting_date'],
                    created_by=request.user
                )
                event.save()
            messages.success(request, 'Meeting Created Successfully.')
            return redirect('hrmMeetings')
    context = {
        'title': 'Meetings',
        'meetings': meetings,
        'form': MeetingForm(),
        'branches': branches,
        'departments': departments,
    }
    if request.user.role == 'Admin':
        return render(request, 'hrm/admin/main/meeting/index.html', context)
    elif request.user.role == 'Manager':
        return render(request, 'hrm/manager/main/meeting/index.html', context)
    elif request.user.role == 'HR':
        return render(request, 'hrm/hr/main/meeting/index.html', context)
    else:
        return redirect('signIn')


@login_required(login_url='signIn')
@admin_manager_hr_role_required
@not_terminated
def hrmMeetingEdit(request, id):
    meeting = get_object_or_404(Meeting, id=id)
    if request.method == 'POST' and 'update_meeting' in request.POST:
        branch_pk = request.POST.get('branch')
        department_pk = request.POST.get('department')

        branch = get_object_or_404(Branch, id=branch_pk)
        department = get_object_or_404(Department, id=department_pk)

        form = MeetingForm(request.POST, instance=meeting)

        if form.is_valid():
            updated_meeting = form.save(commit=False)
            updated_meeting.branch = branch
            updated_meeting.department = department
            updated_meeting.created_by = request.user
            updated_meeting.save()

            # Update Event
            try:
                event = get_object_or_404(Event, meeting=meeting)
                if event:
                    event.meeting = updated_meeting
                    event.title = form.cleaned_data['title']
                    event.branch = form.cleaned_data['branch']
                    event.description = form.cleaned_data['description']
                    event.start_time = form.cleaned_data['meeting_date']
                    event.end_time = form.cleaned_data['meeting_date']
                    event.created_by = request.user
                    event.save()
            except:
                pass

            messages.success(request, 'Meeting Updated Successfully.')
            return redirect('hrmMeetings')


@login_required(login_url='signIn')
@admin_manager_hr_role_required
@not_terminated
def hrmMeetingDelete(request, id):
    meeting = get_object_or_404(Meeting, id=id)

    try:
        event = get_object_or_404(Event, meeting=meeting)
        if event:
            event.delete()
    except:
        pass
    meeting.delete()
    messages.warning(request, 'Meeting Deleted Successfully.')
    return redirect('hrmMeetings')

# ============== Admin Warning View ==============#


@login_required(login_url='signIn')
@not_terminated
def hrmWarnings(request):
    if request.user.role == 'Admin':
        warning_objects = warning.objects.all().order_by('-created_at')
        employees = User.objects.exclude(pk=request.user.pk)
    else:
        warning_objects = warning.objects.filter(
            employee__userprofile__branch=request.user.userprofile.branch).order_by('-created_at')
        employees = User.objects.filter(
            userprofile__branch=request.user.userprofile.branch).exclude(pk=request.user.pk)
        
    if request.method == 'POST' and 'create_warning' in request.POST:
        form = WarningForm(request.POST)
        if form.is_valid():
            new_warning = form.save(commit=False)
            new_warning.created_by = request.user
            new_warning.save()
            messages.success(request, 'Warning Created Successfully.')
            return redirect('hrmWarnings')
    context = {
        'title': 'Warnings',
        'warnings': warning_objects,
        'employees': employees,
        'form': WarningForm(),
    }

    if request.user.role == 'Admin':
        return render(request, 'hrm/admin/main/warning/index.html', context)
    elif request.user.role == 'Manager':
        return render(request, 'hrm/manager/main/warning/index.html', context)
    elif request.user.role == 'HR':
        return render(request, 'hrm/hr/main/warning/index.html', context)
    elif request.user.role == 'Employee':
        return render(request, 'hrm/employee/main/warning/index.html', context)
    else:
        return redirect('signIn')


@login_required(login_url='signIn')
@admin_manager_hr_role_required
@not_terminated
def hrmWarningEdit(request, id):
    warning_object = get_object_or_404(warning, id=id)
    if request.method == 'POST' and 'update_warning' in request.POST:
        employee_pk = request.POST.get('employee')
        employee = get_object_or_404(User, id=employee_pk)

        form = WarningForm(request.POST, instance=warning_object)

        if form.is_valid():
            updated_warning = form.save(commit=False)
            updated_warning.employee = employee
            updated_warning.created_by = request.user
            updated_warning.save()
            messages.success(request, 'Warning Updated Successfully.')
            return redirect('hrmWarnings')


@login_required(login_url='signIn')
@admin_manager_hr_role_required
@not_terminated
def hrmWarningDelete(request, id):
    warning_object = get_object_or_404(warning, id=id)
    warning_object.delete()
    messages.warning(request, 'Warning Deleted Successfully.')
    return redirect('hrmWarnings')

# ============== Admin Termination Type View ==============#


@login_required(login_url='signIn')
@not_terminated
def hrmTerminationTypes(request):
    types = TerminationType.objects.all().order_by('-created_at')

    if request.method == 'POST' and 'create_type' in request.POST:
        form = TerminationTypeForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Termination type created successfully.')
            return redirect('hrmTerminationTypes')

    context = {
        'title': 'Termination Types',
        'types': types,
        'form': TerminationTypeForm()
    }

    if request.user.role == 'Admin':
        return render(request, 'hrm/admin/main/termination/partial/types.html', context)
    elif request.user.role == 'Manager':
        return render(request, 'hrm/manager/main/termination/partial/types.html', context)
    elif request.user.role == 'HR':
        return render(request, 'hrm/hr/main/termination/partial/types.html', context)
    else:
        return redirect('signIn')


@login_required(login_url='signIn')
@admin_manager_hr_role_required
@not_terminated
def hrmTerminationTypeEdit(request, id):
    type = get_object_or_404(TerminationType, id=id)

    if request.method == 'POST' and 'update_type' in request.POST:
        form = TerminationTypeForm(request.POST, instance=type)

        if form.is_valid():
            form.save()
            messages.success(request, 'Termination type updated successfully.')
            return redirect('hrmTerminationTypes')


@login_required(login_url='signIn')
@admin_manager_hr_role_required
@not_terminated
def hrmTerminationTypeDelete(request, id):
    type = get_object_or_404(TerminationType, id=id)
    type.delete()
    messages.warning(request, 'Termination type deleted successfully.')
    return redirect('hrmTerminationTypes')

# ============== Admin Termination View ==============#


@login_required(login_url='signIn')
@not_terminated
def hrmTerminations(request):
    if request.user.role == 'Admin':
        terminations = Termination.objects.all().order_by('-created_at')
        employees = User.objects.exclude(pk=request.user.pk)
    else:
        terminations = Termination.objects.filter(
            employee__userprofile__branch=request.user.userprofile.branch).order_by('-created_at')
        employees = User.objects.filter(
            userprofile__branch=request.user.userprofile.branch).exclude(pk=request.user.pk)

    if request.method == 'POST' and 'create_termination' in request.POST:
        delete_account = request.POST.get('delete-account')
        form = TerminationForm(request.POST)

        if form.is_valid():
            new_termination = form.save(commit=False)
            new_termination.created_by = request.user
            new_termination.save()

            if delete_account:
                employee = get_object_or_404(
                    User, id=new_termination.employee.id)
                employee.delete()
            messages.success(request, 'Terminated Successfully.')
            return redirect('hrmTerminations')
    context = {
        'title': 'Terminations',
        'terminations': terminations,
        'employees': employees,
        'form': TerminationForm(),
    }

    if request.user.role == 'Admin':
        return render(request, 'hrm/admin/main/termination/index.html', context)
    elif request.user.role == 'Manager':
        return render(request, 'hrm/manager/main/termination/index.html', context)
    elif request.user.role == 'HR':
        return render(request, 'hrm/hr/main/termination/index.html', context)
    else:
        return redirect('signIn')


@login_required(login_url='signIn')
@admin_manager_hr_role_required
@not_terminated
def hrmTerminationDelete(request, id):
    termination = get_object_or_404(Termination, id=id)
    if request.user.role == 'Admin' or request.user.role == 'HR' or request.user.role == 'Manager':
        termination.delete()
        messages.warning(request, 'Termination Deleted Successfully.')
    else:
        messages.warning(request, 'Something went wrong.')
    return redirect('hrmTerminations')


# ============== Notification ==============#
@csrf_exempt
def mark_notification_as_read(request, notification_id):
    if request.method == 'POST':
        notification = Notification.objects.get(pk=notification_id)
        notification.readed_by.add(request.user)
        return JsonResponse({'message': 'Notification marked as read.'})
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)
    
    
#==== Attendance =====#
@login_required(login_url='signIn')
def hrmAttendance(request):
    today = date.today()
    user = request.user

    # Fetch the website settings
    website_settings = websiteSetting.objects.first()

    attendance, created = Attendance.objects.get_or_create(employee=user, date=today)
    print('Current Attendance:', attendance)

    clocked_in = attendance.time_in is not None
    clocked_out = attendance.time_out is not None

    if request.GET.get('clock_in') and not clocked_in:
        attendance.time_in = localtime(timezone.now()).time()
        location = request.GET.get('location')
        latitude = request.GET.get('latitude')
        longitude = request.GET.get('longitude')
        if location:
            attendance.location = location
        if latitude:
            attendance.latitude = latitude
        if longitude:
            attendance.longitude = longitude
        
        if website_settings.hrm_attendance_clock_in_max_time:
            max_time = website_settings.hrm_attendance_clock_in_max_time
            if attendance.time_in > max_time:
                attendance.is_late = True
                late_duration = datetime.combine(today, attendance.time_in) - datetime.combine(today, max_time)
                attendance.late_time = str(late_duration)

        attendance.save()
        
        if attendance.is_late:
            late_time_str = attendance.late_time
            late_time_parts = late_time_str.split(':')
            late_hours = int(late_time_parts[0])
            late_minutes = int(late_time_parts[1])
            
            formatted_late_time = f'{late_hours} hours {late_minutes} minutes'
            messages.warning(request, f'Clocked in successfully. You are late by {formatted_late_time}.')
        else:
            messages.success(request, 'Clocked in successfully.')
            
        return redirect('hrmAttendance')

    elif 'clock_out' in request.POST and clocked_in and not clocked_out:
        current_time = localtime(timezone.now()).time()
        if website_settings.hrm_attendance_clock_out_min_time and current_time < website_settings.hrm_attendance_clock_out_min_time:
            formatted_min_time = website_settings.hrm_attendance_clock_out_min_time.strftime('%I:%M %p')
            messages.warning(request, f'You cannot clock out before {formatted_min_time}.')
            return redirect('hrmAttendance')
        
        attendance.time_out = current_time
        time_in = datetime.combine(today, attendance.time_in)
        time_out = datetime.combine(today, attendance.time_out)
        total_hours = time_out - time_in
        total_hours = total_hours.total_seconds() / 3600
        total_hours = round(total_hours, 2)
        attendance.total_hours = total_hours
        
        if website_settings.hrm_attendance_clock_out_min_time and attendance.time_out > website_settings.hrm_attendance_clock_out_min_time:
            over_time_duration = datetime.combine(today, attendance.time_out) - datetime.combine(today, website_settings.hrm_attendance_clock_out_min_time)
            attendance.over_time = str(over_time_duration)

        attendance.save()
        if attendance.over_time:
            over_time_str = attendance.over_time
            over_time_parts = over_time_str.split(':')
            over_time_hours = int(over_time_parts[0])
            over_time_minutes = int(over_time_parts[1])
            
            formatted_over_time = f'{over_time_hours} hours {over_time_minutes} minutes'
            messages.success(request, f'Clocked out successfully. You have worked for {total_hours} hours. Overtime: {formatted_over_time}.')
        else:
            messages.success(request, f'Clocked out successfully. You have worked for {total_hours} hours.')
        return redirect('hrmAttendance')

    context = {
        'title': 'Attendance',
        'attendance': attendance,
        'form': AttendanceForm(),
        'clocked_in': clocked_in,
        'clocked_out': clocked_out,
    }

    if user.role == 'Admin':
        return render(request, 'hrm/admin/main/attendance/index.html', context)
    elif user.role == 'Manager':
        return render(request, 'hrm/manager/main/attendance/index.html', context)
    elif user.role == 'HR':
        return render(request, 'hrm/hr/main/attendance/index.html', context)
    elif user.role == 'Employee':
        return render(request, 'hrm/employee/main/attendance/index.html', context)
    else:
        return redirect('signIn')

#==== Attendance Record By Month And Year =====#
@login_required(login_url='signIn')
def hrmAttendanceRecord(request):
    user = request.user

    if 'filtered_month' not in request.session or 'filtered_year' not in request.session:
        request.session['filtered_month'] = timezone.now().month
        request.session['filtered_year'] = timezone.now().year

    current_month = request.session['filtered_month']
    current_year = request.session['filtered_year']
    year_values = list(range(2020, 2041))


    attendance_records = Attendance.objects.filter(employee=user, date__month=current_month, date__year=current_year)

    if request.method == 'POST':
        if 'filter_attendance' in request.POST:
            month = int(request.POST.get('month'))
            year = int(request.POST.get('year'))

            attendance_records = Attendance.objects.filter(employee=user, date__month=month, date__year=year)
            request.session['filtered_month'] = month
            request.session['filtered_year'] = year

            current_year = year
            current_month = month

            return redirect('hrmAttendanceRecord')

    request.session['filtered_month_expiry'] = (timezone.now() + timedelta(hours=1)).strftime('%Y-%m-%d')
    request.session['filtered_year_expiry'] = (timezone.now() + timedelta(hours=1)).strftime('%Y-%m-%d')

    context = {
        'title': 'Attendance Record',
        'attendance_records': attendance_records,
        'current_month': current_month,
        'current_year': current_year,
        'year_values': year_values,
    }

    # Render the appropriate template based on user role
    if user.role == 'Admin':
        return render(request, 'hrm/admin/main/attendance/record.html', context)
    elif user.role == 'Manager':
        return render(request, 'hrm/manager/main/attendance/record.html', context)
    elif user.role == 'HR':
        return render(request, 'hrm/hr/main/attendance/record.html', context)
    elif user.role == 'Employee':
        return render(request, 'hrm/employee/main/attendance/record.html', context)
    else:
        return redirect('signIn')
    
    
#==== Attendance Record By Date, Month And Year =====#
@login_required(login_url='signIn')
@admin_manager_hr_role_required
def hrmAttendanceRecordByByDateMonthYear(request):
    # Check and initialize session values if they do not exist
    if 'filtered_date' not in request.session or 'filtered_month' not in request.session or 'filtered_year' not in request.session:
        now = timezone.localtime()
        request.session['filtered_date'] = now.day
        request.session['filtered_month'] = now.month
        request.session['filtered_year'] = now.year

    # Fetch current session values
    current_date = request.session.get('filtered_date')
    current_month = request.session.get('filtered_month')
    current_year = request.session.get('filtered_year')

    # Handle POST request
    if request.method == 'POST':
        # Handle date picker form
        if 'filter_attendance_by_data' in request.POST:
            date_str = request.POST.get('date')

            if date_str:
                # Filter by specific date if a date is provided
                try:
                    selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                    date = selected_date.day
                    month = selected_date.month
                    year = selected_date.year

                    # Update session with new date values
                    request.session['filtered_date'] = date
                    request.session['filtered_month'] = month
                    request.session['filtered_year'] = year

                    # Filter attendance based on the selected date
                    attendance_records = Attendance.objects.filter(date__day=date, date__month=month, date__year=year)
                    print('Attendance Records from date:', attendance_records)
                except ValueError:
                    messages.error(request, "Invalid date format. Please select a valid date.")
                    return redirect('hrmAttendanceRecordByByDateMonthYear')

            # Redirect to avoid form resubmission issues
            return redirect('hrmAttendanceRecordByByDateMonthYear')

        # Handle "Filter This Month" button
        elif 'filter_attendance_by_month' in request.POST:
            now = timezone.now()
            month = now.month
            year = now.year

            # Update session with new month and year values
            request.session['filtered_month'] = month
            request.session['filtered_year'] = year

            # Set filtered_date to None because we're filtering by month and year
            request.session['filtered_date'] = None

            # Filter attendance based on the current month and year
            attendance_records = Attendance.objects.filter(date__month=month, date__year=year)
            print('Attendance Records from month:', attendance_records)

            # Redirect to avoid form resubmission issues
            return redirect('hrmAttendanceRecordByByDateMonthYear')

    # Reapply the session-based filtering logic on every page load
    if current_date:
        # Filter by specific date if date is in session
        attendance_records = Attendance.objects.filter(date__day=current_date, date__month=current_month, date__year=current_year)
    else:
        # If date is None, filter by month and year only
        attendance_records = Attendance.objects.filter(date__month=current_month, date__year=current_year)

    print('Attendance Records Final:', attendance_records)

    # Pass context data to the template
    context = {
        'title': 'Attendance',
        'attendance_records': attendance_records,
        'current_date': current_date,
        'current_month': current_month,
        'current_year': current_year
    }

    # Render the appropriate template based on the user's role
    if request.user.role == 'Admin':
        return render(request, 'hrm/admin/main/attendance/all-records.html', context)
    elif request.user.role == 'Manager':
        return render(request, 'hrm/manager/main/attendance/all-records.html', context)
    elif request.user.role == 'HR':
        return render(request, 'hrm/hr/main/attendance/all-records.html', context)



