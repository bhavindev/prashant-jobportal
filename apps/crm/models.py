from django.db import models
from django.utils.text import slugify
from uuid import uuid4
from django.utils import timezone
from django.db.models import Sum
from apps.authapp.models import *
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
import random
import string
from ckeditor.fields import RichTextField


# Product/Services
class items(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='Product_Images/', blank=True, null=True)
    slug = models.SlugField(max_length=300, blank=True, null=True, unique=True)
    description = RichTextField()
    category = models.ForeignKey('itemCategory', on_delete=models.CASCADE)
    unit_type = models.CharField(max_length=100)
    rate = models.FloatField(null=True, blank=True)
    fake_sales = models.IntegerField(null=True, blank=True)
    fake_stars = models.IntegerField(null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)
  
    
    def generate_unique_slug(self, base_slug):
        # Generate a random 3-character string
        random_chars = ''.join(random.choices(string.ascii_lowercase, k=3))
        return f"{base_slug}-{random_chars}"

    def save(self, *args, **kwargs):
        # Generate the initial slug from the item's name
        base_slug = slugify(self.name)
        slug = base_slug
        count = 1

        while items.objects.filter(slug=slug).exists():
            # Slug conflict exists, add an extra number to the slug
            slug = f"{base_slug}-{count}"
            count += 1

        self.slug = slug
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.name
    
# Product/Services Category   
class itemCategory(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=300, blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if self.name:
            original_slug = slugify(self.name)
            queryset = itemCategory.objects.exclude(pk=self.pk)
            slug = original_slug
            counter = 1

            while queryset.filter(slug=slug).exists():
                slug = f"{original_slug}-{counter}"
                counter += 1

            self.slug = slug
            super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

# CRM Projects
class crmProjects(models.Model):
    title = models.CharField(max_length=255)
    progress = models.IntegerField(blank=True, null=True, default=0)
    slug = models.SlugField(max_length=500, blank=True, null=True)
    PROJECT_TYPE_CHOICE = (
        ('client_project', 'Client Project'),
        ('internal_project', 'Internal Project'),
    )
    project_type = models.CharField(max_length=50, choices=PROJECT_TYPE_CHOICE, default='client_project')
    client = models.ForeignKey(Guser, on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField()
    deadline = models.DateField()
    price = models.IntegerField()
    team = models.ManyToManyField(User, related_name='project_team', blank=True)
    
    PROJECT_LABEL_CHOICE = (
        ('started', 'Started'),
        ('completed', 'Completed'),
        ('new_customer', 'New Customer'),
        ('important', 'Important'),
        ('closed', 'Closed'),
        ('running', 'Running'),
        ('canceled', 'Canceled'),
        ('pending', 'Pending'),
    )
    label = models.CharField(max_length=50, choices=PROJECT_LABEL_CHOICE, null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if self.title:
            original_slug = slugify(self.title)
            queryset = crmProjects.objects.exclude(pk=self.pk)
            slug = original_slug
            counter = 1

            while queryset.filter(slug=slug).exists():
                slug = f"{original_slug}-{counter}"
                counter += 1

            self.slug = slug
            super().save(*args, **kwargs)
    
    def get_project_files(self):
        return ProjectFile.objects.filter(project=self)
    
    def __str__(self):
        return self.title

class ProjectFile(models.Model):
    project = models.ForeignKey(crmProjects, on_delete=models.CASCADE)
    upload_file = models.FileField(upload_to='project_files/')
    
# CRM Tasks
class crmTasks(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=300, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    project = models.ForeignKey('crmProjects', on_delete=models.CASCADE)
    STATUS_CHOICES = (
        ('to_do', 'To do'),
        ('in_progress', 'In progress'),
        ('done', 'Done'),
    )
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='to_do')
    PRIORITY_CHOICES = (
        ('minor', 'Minor'),
        ('major', 'Major'),
        ('critical', 'Critical'),
        ('blocker', 'Blocker'),
    )
    priority = models.CharField(max_length=50, choices=PRIORITY_CHOICES, blank=True, null=True)
    PROJECT_LABEL_CHOICE = (
        ('started', 'Started'),
        ('completed', 'Completed'),
        ('new_customer', 'New Customer'),
        ('important', 'Important'),
        ('closed', 'Closed'),
        ('running', 'Running'),
        ('canceled', 'Canceled'),
        ('pending', 'Pending'),
    )
    label = models.CharField(max_length=50, choices=PROJECT_LABEL_CHOICE, null=True, blank=True)
    start_date = models.DateField(blank=True, null=True)
    deadline = models.DateField(blank=True, null=True)
    assigned_to = models.ManyToManyField(User, related_name='task_team', blank=True)
    
    def save(self, *args, **kwargs):
        if self.title:
            original_slug = slugify(self.title)
            queryset = crmTasks.objects.exclude(pk=self.pk)
            slug = original_slug
            counter = 1

            while queryset.filter(slug=slug).exists():
                slug = f"{original_slug}-{counter}"
                counter += 1

            self.slug = slug
            super().save(*args, **kwargs)
    

# CRM Invoice
class Invoice(models.Model):
    STATUS_CHOICES = [
    ('UNPAID', 'UNPAID'),
    ('PARTIALLY_PAID', 'PARTIALLY PAID'),
    ('PAID', 'PAID'),
    ]

    title = models.CharField(null=True, blank=True, max_length=100)
    number = models.CharField(null=True, blank=True, max_length=100)
    billDate = models.DateField(null=True, blank=True)
    dueDate = models.DateField(null=True, blank=True)
    status = models.CharField(choices=STATUS_CHOICES, default='UNPAID', max_length=100)
    discount_amount = models.FloatField(default=0)
    tax_amount = models.FloatField(default=0)
    other_fees_name = models.CharField(max_length=255, default="Other Fees", null=True, blank=True)
    other_fees_amount = models.FloatField(default=0)
    notes = models.TextField(null=True, blank=True, default='This is a computer generated invoice no need signature')

    #RELATED fields
    client = models.ForeignKey(Guser, blank=True, null=True, on_delete=models.SET_NULL)
    project = models.ForeignKey('crmProjects', null=True, on_delete=models.SET_NULL)
    products = models.ManyToManyField('items', related_name='invoice_related_items', blank=True)
    sub_total = models.FloatField(default=0.0, blank=True, null=True)

    #Utility fields
    uniqueId = models.CharField(null=True, blank=True, max_length=100)
    slug = models.SlugField(max_length=500, unique=True, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    last_updated = models.DateTimeField(auto_now=True, blank=True, null=True)


    def __str__(self):
        if self.number:
            return self.number
        else:
            return "None"

    def save(self, *args, **kwargs):
        if self.number:
            self.slug = slugify(self.number)
        if self.uniqueId is None:
            self.uniqueId = str(uuid4()).split('-')[4]
        super().save(*args, **kwargs)
    
    # Get the total of the invoice
    def get_total(self):
        sub_total = self.sub_total or 0
        discount_amount = self.discount_amount or 0
        tax_amount = self.tax_amount or 0
        other_fees_amount = self.other_fees_amount or 0

        total = (sub_total + tax_amount + other_fees_amount) - discount_amount
        return total

    # Delete blank invoices that have been created more than 30 minutes ago
    @classmethod
    def delete_blank_invoices(cls):
        thirty_minutes_ago = timezone.now() - timezone.timedelta(minutes=30)
        blank_invoices_to_delete = cls.objects.filter(
            products__isnull=True,
            date_created__lt=thirty_minutes_ago
        )

        for invoice in blank_invoices_to_delete:
            invoice.delete()
    
    # Get the status of the invoice
    def get_status(self):
        # Check if the invoice is overdue based on the date
        if self.dueDate is not None and self.dueDate < timezone.now().date():
            if self.status != 'PAID':
                self.status = 'OVERDUE'

        # Set default values for sub_total, discount_amount, tax_amount, and other_fees_amount
        total_product_price = self.sub_total or 0
        discount_amount = self.discount_amount or 0
        tax_amount = self.tax_amount or 0
        other_fees_amount = self.other_fees_amount or 0

        # Calculate total after subtracting discount
        total_product_price -= discount_amount
        total_product_price += tax_amount + other_fees_amount

        total_payments = self.payments.aggregate(total=Sum('payment_ammount'))['total'] or 0

        # Calculate the balance
        balance = total_product_price - total_payments

        if balance == 0 and total_payments > 0:
            self.status = 'PAID'
        elif balance > 0 and total_payments > 0:
            self.status = 'PARTIALLY_PAID'
        elif balance > 0 and total_payments == 0:
            if self.dueDate is None or self.dueDate >= timezone.now().date():
                self.status = 'UNPAID'
            else:
                self.status = 'OVERDUE'

        self.save()

        display_value = dict(self.STATUS_CHOICES).get(self.status, '')

        return {"status": self.status, "status_display": display_value, "balance": balance}


    
class InvoiceItem(models.Model):
    invoice = models.ForeignKey('Invoice', on_delete=models.CASCADE)
    item = models.ForeignKey('items', on_delete=models.CASCADE)
    unit_type = models.CharField(max_length=200, blank=True, null=True)
    quantity = models.IntegerField(default=1)
    unit_price = models.FloatField(default=0.0)
    sub_total = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.item.name} - Quantity: {self.quantity} - Invoice: #{self.invoice}"

   
# CRM Payments
class Payments(models.Model):
    invoice = models.ForeignKey('Invoice', blank=True, null=True, on_delete=models.CASCADE, related_name='payments')
    title = models.CharField(max_length=200, blank=True, null=True)
    slug = models.SlugField(max_length=200, blank=True, null=True)
    payment_method = models.CharField(max_length=255, blank=True, null=True)
    payment_ammount = models.FloatField(blank=True, null=True)
    transaction_id = models.CharField(max_length=255, blank=True, null=True)
    payment_date = models.DateField(blank=True, null=True)
    payment_note = models.TextField(blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if self.title:
            original_slug = slugify(self.title)
            queryset = Payments.objects.exclude(pk=self.pk)
            slug = original_slug
            counter = 1

            while queryset.filter(slug=slug).exists():
                slug = f"{original_slug}-{counter}"
                counter += 1

            self.slug = slug
            super().save(*args, **kwargs)
            
    def __str__(self):
        return f"Invoice: {self.invoice}, Title: {self.title}"

# Create a dictionary to map payments to their years
payment_years = {}

class YearlyPaymentStatistics(models.Model):
    year = models.PositiveIntegerField(unique=True)
    total_payment = models.BigIntegerField(default=0)

@receiver(post_save, sender=Payments)
@receiver(pre_save, sender=Payments)
def update_yearly_statistics(sender, instance, **kwargs):
    year = payment_years.get(instance.id, None)  # Get the year from the dictionary
    if year is not None:
        total_payment_for_year = Payments.objects.filter(payment_date__year=year).aggregate(Sum('payment_ammount'))['payment_ammount__sum'] or 0
        obj, created = YearlyPaymentStatistics.objects.get_or_create(year=year)
        obj.total_payment = total_payment_for_year
        obj.save()

# Update the dictionary when a new payment is added or when its year is modified
@receiver(post_save, sender=Payments)
@receiver(pre_save, sender=Payments)
def update_payment_year(sender, instance, **kwargs):
    if instance.payment_date:
        payment_years[instance.id] = instance.payment_date.year

# Remove entries from the dictionary when payments are deleted
@receiver(models.signals.post_delete, sender=Payments)
def remove_payment_year(sender, instance, **kwargs):
    payment_years.pop(instance.id, None)

# CRM Expense
class Expense(models.Model):
    date_of_expense = models.DateField(blank=True, null=True)
    EXPENSE_TYPE = (
    ('rent/mortgage', 'Rent/Mortgage'),
    ('utilities', 'Utilities'),
    ('transportation', 'Transportation'),
    ('food_and_dining', 'Food and Dining'),
    ('insurance', 'Insurance'),
    ('taxes', 'Taxes'),
    ('debt_payments', 'Debt Payments'),
    ('healthcare_and_medical_expenses', 'Healthcare and Medical Expenses'),
    ('miscellaneous_expenses', 'Miscellaneous Expenses'),
    ('personal_care', 'Personal Care'),
    ('fees', 'Fees'),
    ('others', 'Others'),
)
    category = models.CharField(max_length=255, blank=True, null=True, choices=EXPENSE_TYPE)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=500, blank=True, null=True)
    amount = models.FloatField()
    description = models.TextField(blank=True, null=True)
            
    def save(self, *args, **kwargs):
        if self.title:
            original_slug = slugify(self.title)
            queryset = Expense.objects.exclude(pk=self.pk)
            slug = original_slug
            counter = 1

            while queryset.filter(slug=slug).exists():
                slug = f"{original_slug}-{counter}"
                counter += 1

            self.slug = slug
            super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title


        

            
