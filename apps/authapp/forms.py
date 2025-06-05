import os
from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from apps.authapp.models import UserProfile,User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django_recaptcha.fields import ReCaptchaField

class UserProfileForm(forms.ModelForm):
    role = forms.ChoiceField(choices=get_user_model().Role.choices, required=False) 
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        excluded_roles = ['Manager', 'HR', 'Employee']
        if 'instance' in kwargs:
            user = kwargs['instance'].user
            self.fields['role'].initial = user.role
        self.fields['role'].choices = [
            (key, value) for key, value in get_user_model().Role.choices if value not in excluded_roles
        ]

    class Meta:
        model = UserProfile
        fields = ('profile_picture', 'name', 'slug', 'role', 'email', 'phone', 'address', 'city', 'state', 'country', 'zipcode', 'facebook', 'instagram', 'linkedin')
        widgets = {
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-select'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'zipcode': forms.TextInput(attrs={'class': 'form-control'}),
            'facebook': forms.TextInput(attrs={'class': 'form-control'}),
            'instagram': forms.TextInput(attrs={'class': 'form-control'}),
            'linkedin': forms.TextInput(attrs={'class': 'form-control'}),
        }
        
    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            user = instance.user
            new_role = self.cleaned_data['role']

            if new_role:  # Check if a new role is selected
                user.role = new_role
                user.save()

            instance.save()
        return instance

class UserPasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = User
    
class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username', 'required':'required'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={ 'class': 'form-control', 'name': 'login[password]', 'required': 'required', 'placeholder': '*********'}))
    if os.getenv('SHOW_RECAPTCHA') == 'True':
        captcha = ReCaptchaField()
    
class CustomUserCreationForm(UserCreationForm):
    name = forms.CharField(max_length=255)
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    role = forms.ChoiceField(choices=[], widget=forms.Select(attrs={'class': 'form-select'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        excluded_roles = ['Manager', 'HR', 'Employee']
        if 'instance' in kwargs:
            user = kwargs['instance'].user
            self.fields['role'].initial = user.role
        self.fields['role'].choices = [
            (key, value) for key, value in get_user_model().Role.choices if value not in excluded_roles
        ]

    class Meta:
        model = get_user_model()
        fields = ['name', 'username', 'password1', 'password2', 'email', 'role']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }


