from django.contrib import admin
from apps.authapp.models import *
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Modify this class
class UserAdmin(BaseUserAdmin):
    list_display = (
        'username',
        'email',
        'is_verified',
        'role',
        'created',
    )
    list_filter = (
        'is_superuser',
        'is_verified',
        'created',
        'role'
    )
    search_fields = ('username', 'email')

    # Add the is_verified field to the fieldsets
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'is_verified', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

# Register your User model with the modified UserAdmin class
admin.site.register(User, UserAdmin)

class GUserAdmin(BaseUserAdmin):
    list_display = (
        'username',
        'email',
        'is_verified',
        'role',
        'created',
    )
    
    search_fields = ('username', 'email')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'is_verified', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    def get_queryset(self, request):
        return User.objects.filter(role=User.Role.Guser)

admin.site.register(Guser, GUserAdmin)

class ManagerAdmin(BaseUserAdmin):
    list_display = (
        'username',
        'email',
        'is_verified',
        'role',
        'created',
    )
    
    search_fields = ('username', 'email')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'is_verified', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    def get_queryset(self, request):
        return User.objects.filter(role=User.Role.Manager)

admin.site.register(Manager, ManagerAdmin)

class HRAdmin(BaseUserAdmin):
    list_display = (
        'username',
        'email',
        'is_verified',
        'role',
        'created',
    )
    
    search_fields = ('username', 'email')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'is_verified', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    def get_queryset(self, request):
        return User.objects.filter(role=User.Role.Hr)

admin.site.register(Hr, HRAdmin)

class EmployeeAdmin(BaseUserAdmin):
    list_display = (
        'username',
        'email',
        'is_verified',
        'role',
        'created',
    )
    
    search_fields = ('username', 'email')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'is_verified', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    def get_queryset(self, request):
        return User.objects.filter(role=User.Role.Employee)

admin.site.register(Employee, EmployeeAdmin)
    
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'email', 'phone', 'profile_picture')

admin.site.register(PasswordResetToken)
