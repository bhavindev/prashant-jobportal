from django.forms import ModelForm, DateInput
from apps.hrm.models import *
from apps.authapp.models import UserProfile
from django import forms

# Event Form
class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ["title", "description", "start_time", "end_time", "branch"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter event title"}),
            "branch": forms.Select(attrs={"class": "form-control", "id": "branchadd"}),
            "description": forms.Textarea(attrs={"class": "form-control", "placeholder": "Enter event description", "rows": 3}),
            "start_time": DateInput(attrs={"type": "date", "class": "form-control"}, format="%Y-%m-%d"),
            "end_time": DateInput(attrs={"type": "date", "class": "form-control"}, format="%Y-%m-%d"),
        }

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.fields["start_time"].input_formats = ("%Y-%m-%d",)
        self.fields["end_time"].input_formats = ("%Y-%m-%d",)
        
# HRM Branch, Department, Designation, Job Type Form
class bDDJform(forms.ModelForm):
    class Meta:
        model = UserProfile  # Specify the model for the form
        fields = ['branch', 'department', 'designation', 'job_type']
        widgets = {
            'branch': forms.Select(attrs={'class': 'form-control', 'id' : 'yourSelectInput', 'required' : 'required'}),
            'department': forms.Select(attrs={'class': 'form-control', 'id' : 'yourSelectInput1', 'required' : 'required'}),
            'designation': forms.Select(attrs={'class': 'form-control', 'id' : 'yourSelectInput2', 'required' : 'required'}),
            'job_type': forms.Select(attrs={'class': 'form-control', 'id' : 'yourSelectInput3', 'required' : 'required'}),
        }
        
# Staff Profile Form
class StaffProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = '__all__'
        exclude = ['user']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        select_fields = ['branch', 'department', 'designation', 'job_type']

        for field_name, field in self.fields.items():
            if field_name not in select_fields:
                if 'class' in field.widget.attrs:
                    field.widget.attrs['class'] += ' form-control'
                else:
                    field.widget.attrs['class'] = 'form-control'
            
            if field_name in select_fields:
                if 'class' in field.widget.attrs:
                    field.widget.attrs['class'] += ' form-select select2'
                else:
                    field.widget.attrs['class'] = 'form-select select2'

# HRM Branch Form
class BranchForm(forms.ModelForm):
    class Meta:
        model = Branch
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            
# HRM Department Form
class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            
# HRM Designation Form
class DesignationForm(forms.ModelForm):
    class Meta:
        model = Designation
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            
# HRM Job Type Form
class JobTypeForm(forms.ModelForm):
    class Meta:
        model = JobType
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            
# HRM Notice Form
class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = '__all__'
        widgets = {
            'branch': forms.Select(attrs={'id' : 'branchadd', 'required' : 'required'}),
            'department': forms.Select(attrs={'id' : 'departmentadd'}),
            'description': forms.Textarea(attrs={'rows' : 4}),
            'start_date': forms.DateInput(attrs={'type' : 'date'}),
            'end_date': forms.DateInput(attrs={'type' : 'date'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            
# HRM Holiday Form
class HolidayForm(forms.ModelForm):
    class Meta:
        model = Holiday
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'rows' : 4}),
            'branch': forms.Select(attrs={'id' : 'branchadd', 'required' : 'required'}),
            'start_date': forms.DateInput(attrs={'type' : 'date'}),
            'end_date': forms.DateInput(attrs={'type' : 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            
# HRM Leave Type Form
class LeaveTypeForm(forms.ModelForm):
    class Meta:
        model = LeaveType
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            
# HRM Leave Form
class LeaveForm(forms.ModelForm):
    class Meta:
        model = Leave
        fields = '__all__'
        widgets = {
            'employee': forms.Select(attrs={'id' : 'employeeadd', 'required' : 'required'}),
            'status' : forms.Select(attrs={'id' : 'statusadd', 'required' : 'required'}),
            'leave_type' : forms.Select(attrs={'id' : 'ltadd', 'required' : 'required'}),
            'reason': forms.Textarea(attrs={'rows' : 4}),
            'start_date': forms.DateInput(attrs={'type' : 'date'}),
            'end_date': forms.DateInput(attrs={'type' : 'date'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

# HRM Leave Form
class LeaveRequestForm(forms.ModelForm):
    class Meta:
        model = Leave
        fields = '__all__'
        exclude = ['status', 'created_by', 'employee']
        widgets = {
            'leave_type' : forms.Select(attrs={'id' : 'ltadd', 'required' : 'required'}),
            'reason': forms.Textarea(attrs={'rows' : 4}),
            'start_date': forms.DateInput(attrs={'type' : 'date'}),
            'end_date': forms.DateInput(attrs={'type' : 'date'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            
# HRM Meeting Form
class MeetingForm(forms.ModelForm):
    class Meta:
        model = Meeting
        fields = '__all__'
        widgets = {
            'branch': forms.Select(attrs={'id' : 'branchadd', 'required' : 'required'}),
            'department': forms.Select(attrs={'id' : 'departmentadd'}),
            'meeting_type' : forms.Select(attrs={'id' : 'mtadd', 'required' : 'required'}),
            'description': forms.Textarea(attrs={'rows' : 3}),
            'meeting_date': forms.DateInput(attrs={'type' : 'date'}),
            'meeting_time': forms.DateInput(attrs={'type' : 'time'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            
# HRM Warning Form
class WarningForm(forms.ModelForm):
    class Meta:
        model = warning
        fields = '__all__'
        widgets = {
            'employee': forms.Select(attrs={'id' : 'employeeadd', 'required' : 'required', 'class' : 'form-control'}),
            'reason': forms.Textarea(attrs={'rows' : 3, 'required' : 'required', 'class' : 'form-control'}),
        }

# HRM Termination Type Form
class TerminationTypeForm(forms.ModelForm):
    class Meta:
        model = TerminationType
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
 
# HRM Termination Form
class TerminationForm(forms.ModelForm):
    class Meta:
        model = Termination
        fields = '__all__'
        widgets = {
            'employee': forms.Select(attrs={'id' : 'employeeadd', 'required' : 'required', 'class' : 'form-control'}),
            'termination_type' : forms.Select(attrs={'id' : 'ttadd', 'required' : 'required', 'class' : 'form-control'}),
            'reason': forms.Textarea(attrs={'rows' : 3, 'required' : 'required', 'class' : 'form-control'}),
        }

# HRM Payroll Form
class PayrollForm(forms.ModelForm):
    class Meta:
        model = Payroll
        fields = '__all__'
        widgets = {
            'employee': forms.Select(attrs={'id' : 'employeeadd', 'required' : 'required', 'class' : 'form-control'}),
        }
            
# HRM Salary Form
class SalaryForm(forms.ModelForm):
    class Meta:
        model = BasicSalary
        fields = '__all__'
        exclude = ['payroll']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            
# HRM Allowance Form
class AllowanceForm(forms.ModelForm):
    class Meta:
        model = Allowance
        fields = '__all__'
        exclude = ['payroll']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            
# HRM Deduction Form
class DeductionForm(forms.ModelForm):
    class Meta:
        model = Deduction
        fields = '__all__'
        exclude = ['payroll']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            
#=== Attendance Form ===
class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = '__all__'
        widgets = {
            'employee': forms.Select(attrs={'id' : 'employeeadd', 'required' : 'required', 'class' : 'form-control'}),
            'status': forms.Select(attrs={'id' : 'statusadd', 'required' : 'required', 'class' : 'form-control'}),
            'date': forms.DateInput(attrs={'type' : 'date', 'class' : 'form-control'}),
            'time_in': forms.TimeInput(attrs={'type' : 'time', 'class' : 'form-control'}),
            'time_out': forms.TimeInput(attrs={'type' : 'time', 'class' : 'form-control'}),
        }