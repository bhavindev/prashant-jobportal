from django import forms
from apps.legals.models import *

# Term Form
class termsForm(forms.ModelForm):
    class Meta:
        model = termsnConditionPage
        fields = '__all__'
        exclude = ['language']

class termsPageSeoForm(forms.ModelForm):
    class Meta:
        model = termsnConditionPageSEO
        fields = '__all__'
        exclude = ['language']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to form fields
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

# Policy Form       
class policyForm(forms.ModelForm):
    class Meta:
        model = privacyPolicyPage
        fields = '__all__'
        exclude = ['language']

class policyPageSeoForm(forms.ModelForm):
    class Meta:
        model = privacyPolicyPageSEO
        fields = '__all__'
        exclude = ['language']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to form fields
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

# Agreement Form
class agreementForm(forms.ModelForm):
    class Meta:
        model = agreement
        fields = ['service','name','phone','email','address','city','state','postal','is_signed']
        widgets = {
            'service': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Select a service', 'required': 'required'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your name', 'required': 'required'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your phone number', 'required': 'required'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your email', 'required': 'required'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your address', 'required': 'required'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your city', 'required': 'required'}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your state', 'required': 'required'}),
            'postal': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your postal code', 'required': 'required'}),
            'is_signed': forms.CheckboxInput(attrs={'class': 'form-check-input', 'required': 'required'}),
        }
        
class agreementStatusForm(forms.ModelForm):
    class Meta:
        model = agreement
        fields = ['is_approved']
        widgets = {
            'is_approved' : forms.CheckboxInput(attrs={'data-bs-original-title': '', 'title': ''}),
        }


