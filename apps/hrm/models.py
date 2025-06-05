from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from datetime import datetime

# ========= Notification =========#
class Notification(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    branch = models.ForeignKey('hrm.Branch', on_delete=models.CASCADE, blank=True, null=True, related_name='notification_branch')
    department = models.ForeignKey('hrm.Department', on_delete=models.CASCADE, blank=True, null=True, related_name='notification_department')
    readed_by = models.ManyToManyField('authapp.User', blank=True)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title

# ========= Branch =========#


class Branch(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True)
    address = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    created_at = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.name:
            original_slug = slugify(self.name)
            queryset = Branch.objects.exclude(pk=self.pk)
            slug = original_slug
            counter = 1

            while queryset.filter(slug=slug).exists():
                slug = f"{original_slug}-{counter}"
                counter += 1

            self.slug = slug
            super().save(*args, **kwargs)

    def __str__(self):
        return self.name

# ========= Department =========#


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.name:
            original_slug = slugify(self.name)
            queryset = Department.objects.exclude(pk=self.pk)
            slug = original_slug
            counter = 1

            while queryset.filter(slug=slug).exists():
                slug = f"{original_slug}-{counter}"
                counter += 1

            self.slug = slug
            super().save(*args, **kwargs)

    def __str__(self):
        return self.name

# ========= Designation =========#


class Designation(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.name:
            original_slug = slugify(self.name)
            queryset = Designation.objects.exclude(pk=self.pk)
            slug = original_slug
            counter = 1

            while queryset.filter(slug=slug).exists():
                slug = f"{original_slug}-{counter}"
                counter += 1

            self.slug = slug
            super().save(*args, **kwargs)

    def __str__(self):
        return self.name

# ========= Leave Type =========#


class LeaveType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.name:
            original_slug = slugify(self.name)
            queryset = LeaveType.objects.exclude(pk=self.pk)
            slug = original_slug
            counter = 1

            while queryset.filter(slug=slug).exists():
                slug = f"{original_slug}-{counter}"
                counter += 1

            self.slug = slug
            super().save(*args, **kwargs)

    def __str__(self):
        return self.name

# ========= Leave ==========#


class Leave(models.Model):
    employee = models.ForeignKey('authapp.User', on_delete=models.CASCADE)
    leave_type = models.ForeignKey(LeaveType, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    STATUS_CHOISE = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    )
    status = models.CharField(
        max_length=100, choices=STATUS_CHOISE, default='Pending')
    created_at = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey(
        'authapp.User', on_delete=models.CASCADE, blank=True, null=True, related_name='leave_created_by')

    def get_status(self):
        if self.status == 'Pending':
            return 'warning'
        elif self.status == 'Approved':
            return 'success'
        elif self.status == 'Rejected':
            return 'danger'

    def __str__(self):
        return self.employee.username


# ========= Payroll =========#


class Payroll(models.Model):
    employee = models.ForeignKey('authapp.User', on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.employee.username


# ========= Allowance =========#


class Allowance(models.Model):
    payroll = models.ForeignKey(Payroll, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    amount = models.FloatField()
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.payroll.employee.username
    

# ========= Deduction =========#


class Deduction(models.Model):
    payroll = models.ForeignKey(Payroll, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    amount = models.FloatField()
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.payroll.employee.username

# ========= Salary =========#
    
class BasicSalary(models.Model):
    payroll = models.ForeignKey(Payroll, on_delete=models.CASCADE)
    SALARY_TYPES = (
        ('Monthly', 'Monthly'),
        ('Weekly', 'Weekly'),
        ('Daily', 'Daily'),
        ('Yearly', 'Yearly'),
        ('Hourly', 'Hourly'),
        ('Bi-monthly', 'Bi-monthly'),
        ('Commission-based', 'Commission-based'),
        ('Contract-based', 'Contract-based'),
        ('Retainer-based', 'Retainer-based'),
        ('Profit-sharing', 'Profit-sharing'),
    )
    type = models.CharField(max_length=50, choices=SALARY_TYPES, default='Monthly')
    amount = models.FloatField()
    created_at = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey('authapp.User', on_delete=models.CASCADE, blank=True, null=True, related_name='salary_created_by')

    def __str__(self):
        return self.payroll.employee.username


# ========= Payslip =========#
class Payslip(models.Model):
    payroll = models.ForeignKey(Payroll, on_delete=models.CASCADE)
    STATUS_CHOISE = (
        ('Paid', 'Paid'),
        ('Unpaid', 'Unpaid'),
    )
    status = models.CharField(max_length=50, choices=STATUS_CHOISE, default='Unpaid')
    date = models.DateField()
    created_at = models.DateField(auto_now_add=True)
    
    def get_status(self):
        if self.status == 'Paid':
            return 'success'
        if self.status == 'Unpaid':
            return 'danger'

    def __str__(self):
        return self.payroll.employee.username    

# ========= Termination Type =========#
class TerminationType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.name:
            original_slug = slugify(self.name)
            queryset = TerminationType.objects.exclude(pk=self.pk)
            slug = original_slug
            counter = 1

            while queryset.filter(slug=slug).exists():
                slug = f"{original_slug}-{counter}"
                counter += 1

            self.slug = slug
            super().save(*args, **kwargs)

    def __str__(self):
        return self.name

# ========= Termination =========#


class Termination(models.Model):
    employee = models.ForeignKey('authapp.User', on_delete=models.CASCADE)
    termination_type = models.ForeignKey(
        TerminationType, on_delete=models.CASCADE)
    reason = models.TextField()
    created_by = models.ForeignKey('authapp.User', on_delete=models.CASCADE,
                                   blank=True, null=True, related_name='termination_created_by')
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.employee.username

# ========= Warning =========#


class warning(models.Model):
    employee = models.ForeignKey('authapp.User', on_delete=models.CASCADE)
    reason = models.TextField()
    created_at = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey('authapp.User', on_delete=models.CASCADE,
                                   blank=True, null=True, related_name='warning_created_by')

    def __str__(self):
        return self.employee.username

# ========= Job Type =========#


class JobType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.name:
            original_slug = slugify(self.name)
            queryset = JobType.objects.exclude(pk=self.pk)
            slug = original_slug
            counter = 1

            while queryset.filter(slug=slug).exists():
                slug = f"{original_slug}-{counter}"
                counter += 1

            self.slug = slug
            super().save(*args, **kwargs)

    def __str__(self):
        return self.name

# ========= Meeting =========#


class Meeting(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, blank=True, null=True)
    meeting_date = models.DateField()
    meeting_time = models.TimeField()
    description = models.TextField(blank=True, null=True)
    TYPE_CHOISE = (
        ('Offline', 'Offline'),
        ('Online', 'Online'),
    )
    meeting_type = models.CharField(
        max_length=100, choices=TYPE_CHOISE, default='Offline')
    meeting_link = models.CharField(
        max_length=300, blank=True, null=True, default='#')
    created_at = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey('authapp.User', on_delete=models.CASCADE,
                                   blank=True, null=True, related_name='meeting_created_by')

    def __str__(self):
        return f'{self.branch.name} Meeting - {self.meeting_date} {self.meeting_time}'

# ========= Notice =========#


class Notice(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, blank=True, null=True)
    created_by = models.ForeignKey(
        'authapp.User', on_delete=models.CASCADE, blank=True, null=True, related_name='notice_created_by')
    title = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f'{self.branch.name} Branch Notice - {self.title}'

# ========= Holiday =========#


class Holiday(models.Model):
    occasion = models.CharField(max_length=100)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    created_by = models.ForeignKey('authapp.User', on_delete=models.CASCADE,
                                   blank=True, null=True, related_name='holiday_created_by')
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'Holiday - {self.occasion}'

# ========= Event =========#


class EventManager(models.Manager):
    """ Event manager """

    def get_all_events(self):
        events = Event.objects.filter(is_active=True)
        return events

    def get_running_events(self):
        running_events = Event.objects.filter(
            is_active=True, end_time__gte=datetime.now().date(),).order_by("start_time")
        return running_events


class Event(models.Model):
    """ Event model """

    title = models.CharField(max_length=200)
    branch = models.ForeignKey(
        Branch, on_delete=models.CASCADE, blank=True, null=True)
    created_by = models.ForeignKey(
        'authapp.User', on_delete=models.CASCADE, blank=True, null=True)
    description = models.TextField()
    start_time = models.DateField()
    end_time = models.DateField()

    is_active = models.BooleanField(default=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    notice = models.ForeignKey(
        Notice, on_delete=models.CASCADE, blank=True, null=True)
    meeting = models.ForeignKey(
        Meeting, on_delete=models.CASCADE, blank=True, null=True)
    holiday = models.ForeignKey(
        Holiday, on_delete=models.CASCADE, blank=True, null=True)

    objects = EventManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("hrm:event-detail", args=(self.id,))

    @property
    def get_html_url(self):
        url = reverse("hrm:event-detail", args=(self.id,))
        return f'<a href="{url}"> {self.title} </a>'

#==== Attendance =====#
class Attendance(models.Model):
    employee = models.ForeignKey('authapp.User', on_delete=models.CASCADE)
    date = models.DateField()
    time_in = models.TimeField(blank=True, null=True)
    time_out = models.TimeField(blank=True, null=True)
    total_hours = models.FloatField(blank=True, null=True)
    is_late = models.BooleanField(default=False)
    late_time = models.CharField(max_length=100, blank=True, null=True)
    over_time = models.CharField(max_length=100, blank=True, null=True)
    latitude = models.CharField(max_length=100, blank=True, null=True)
    longitude = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.employee.username