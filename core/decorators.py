from django.http import Http404
from functools import wraps
from apps.hrm.models import Termination
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import logout

def admin_role_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == 'Admin':  
            return view_func(request, *args, **kwargs)
        else:
            raise Http404("Page not found")
    return _wrapped_view

def user_role_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == 'User':
            return view_func(request, *args, **kwargs)
        else:
            raise Http404("Page not fount")
    return _wrapped_view


def both_role_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == 'Admin' or request.user.role == 'Editor':
            return view_func(request, *args, **kwargs)
        else:
            raise Http404("Page not fount")
    return _wrapped_view

def manager_role_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == 'Manager':  
            return view_func(request, *args, **kwargs)
        else:
            raise Http404("Page not found")
    return _wrapped_view

def hr_role_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == 'HR':  
            return view_func(request, *args, **kwargs)
        else:
            raise Http404("Page not found")
    return _wrapped_view

def employee_role_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == 'Employee':  
            return view_func(request, *args, **kwargs)
        else:
            raise Http404("Page not found")
    return _wrapped_view

def admin_manager_role_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == 'Admin' or request.user.role == 'Manager':
            return view_func(request, *args, **kwargs)
        else:
            raise Http404("Page not fount")
    return _wrapped_view

def admin_manager_hr_role_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == 'Admin' or request.user.role == 'Manager' or request.user.role == 'HR':
            return view_func(request, *args, **kwargs)
        else:
            raise Http404("Page not fount")
    return _wrapped_view

def not_terminated(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        terminated = Termination.objects.filter(employee=request.user).exists()
        if terminated:
            logout(request)
            messages.warning(request, 'Your account has been terminated')
            return redirect('signIn')
        return view_func(request, *args, **kwargs)
    return _wrapped_view