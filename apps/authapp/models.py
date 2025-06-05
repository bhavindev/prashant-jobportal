from django.db import models
from django.contrib.auth.models import AbstractUser
from apps.authapp.manager import UserManager 
from django.contrib.auth.models import BaseUserManager
from django.utils.text import slugify
from django.db.models.signals import post_save 
from django.dispatch import receiver
from django.utils import timezone
import uuid
from apps.hrm.models import *

class User(AbstractUser):
   class Role(models.TextChoices):
      Admin = 'Admin',"Admin"
      Guser = 'User',"User"
      Editor = 'Editor',"Editor"
      Manager = 'Manager',"Manager"  
      Hr = 'HR',"HR"
      Employee = 'Employee',"Employee"
      
   is_verified = models.BooleanField(default=False , verbose_name='Is Verified')
   role = models.CharField(max_length=255, verbose_name='Role' , choices=Role.choices, blank=True, null=True)
   created = models.DateField(auto_now_add=True)
   is_Vrified = models.BooleanField(default=False)
   base_role = Role.Admin

   objects = UserManager()

   def save(self, *args, **kwargs):
    if not self.pk and not self.role:
        self.role = self.base_role
    return super().save(*args, **kwargs)

   def __str__(self):
      return self.username

# manager
class CustomerUserManager(BaseUserManager):
    def get_queryset(self ,*args, **kwargs) :
        reasult =  super().get_queryset(*args, **kwargs)
        return reasult.filter(role=User.Role.Guser)
    
   
    def create_user(self, email, password=None, **extra_fields):
        if  not email :
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save()
        return user

#proxy model
class Guser(User):
   base_role = User.Role.Guser
   objects = CustomerUserManager()
   class Meta:
      proxy = True

# Manager , HR, Employee proxy model
class ManagerManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(role=User.Role.Manager)
    
    def create_user(self, email, password=None, **extra_fields):
        if  not email :
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save()
        return user

class Manager(User):
    base_role = User.Role.Manager
    objects = ManagerManager()

    class Meta:
        proxy = True

class HrManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(role=User.Role.Hr)
    
    def create_user(self, email, password=None, **extra_fields):
        if  not email :
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save()
        return user

class Hr(User):
    base_role = User.Role.Hr
    objects = HrManager()

    class Meta:
        proxy = True

class EmployeeManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(role=User.Role.Employee)
    
    def create_user(self, email, password=None, **extra_fields):
        if  not email :
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save()
        return user

class Employee(User):
    base_role = User.Role.Employee
    objects = EmployeeManager()

    class Meta:
        proxy = True



# User Profile
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='user_pictures/', blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    slug = models.SlugField(max_length=255, blank=True, null=True)
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, blank=True, null=True)
    designation = models.ForeignKey(Designation, on_delete=models.SET_NULL, blank=True, null=True)
    job_type = models.ForeignKey(JobType, on_delete=models.SET_NULL, blank=True, null=True)
    email = models.EmailField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    zipcode = models.CharField(max_length=255, blank=True, null=True)
    facebook = models.CharField(max_length=255, blank=True, null=True)
    instagram = models.CharField(max_length=255, blank=True, null=True)
    linkedin = models.CharField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.pk:
            original_profile = UserProfile.objects.get(pk=self.pk)
            if original_profile.user.email != self.email:
                original_profile.user.email = self.email
                original_profile.user.save()
                
        self.slug = slugify(self.user.username)
        super(UserProfile, self).save(*args, **kwargs)
        
    def getUserImage(self):
      image_url = ""
      if self.profile_picture:
         image_url = self.profile_picture.url
      else:
         image_url = "https://cdn-icons-png.flaticon.com/128/3135/3135715.png"
      return image_url

    def __str__(self):
        return self.user.username

# Password reset token generate
class PasswordResetToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expiration_time = models.DateTimeField() 

    def __str__(self):
        return str(self.token)

    def is_expired(self):
        now = timezone.now()
        return now > self.expiration_time
    
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(
            user=instance,
            email=instance.email,
            name=instance.username,
            slug=slugify(instance.username),
        )

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()

# signals for User
@receiver(post_save, sender=User)
def create_customer_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)

@receiver(post_save, sender=User)
def save_customer_profile(sender, instance, **kwargs):
    if hasattr(instance, 'userprofile'):
        instance.userprofile.save()

# signals for Guser
@receiver(post_save, sender=Guser)
def create_customer_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(
            user=instance, 
            email=instance.email,
            name=instance.username,
            slug=slugify(instance.username),
        )

@receiver(post_save, sender=Guser)
def save_customer_profile(sender, instance, **kwargs):
    if hasattr(instance, 'userprofile'):
        instance.userprofile.save()
        
# Signals for Employee
@receiver(post_save, sender=Employee)
def create_customer_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(
            user=instance, 
            email=instance.email,
            name=instance.username,
            slug=slugify(instance.username),
        )

@receiver(post_save, sender=Employee)
def save_customer_profile(sender, instance, **kwargs):
    if hasattr(instance, 'userprofile'):
        instance.userprofile.save()
        
# Signals for Manager
@receiver(post_save, sender=Manager)
def create_customer_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(
            user=instance, 
            email=instance.email,
            name=instance.username,
            slug=slugify(instance.username),
        )

@receiver(post_save, sender=Manager)
def save_customer_profile(sender, instance, **kwargs):
    if hasattr(instance, 'userprofile'):
        instance.userprofile.save()
        
# Signals for HR
@receiver(post_save, sender=Hr)
def create_customer_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(
            user=instance, 
            email=instance.email,
            name=instance.username,
            slug=slugify(instance.username),
        )

@receiver(post_save, sender=Hr)
def save_customer_profile(sender, instance, **kwargs):
    if hasattr(instance, 'userprofile'):
        instance.userprofile.save()
        