from django import forms
from apps.crm.models import *
from typing import List, Tuple
from apps.authapp.models import User

# Item Form
class CRMItemForm(forms.ModelForm):
    class Meta:
        model = items
        fields = '__all__'
        widgets = {
            'image' : forms.FileInput(attrs={'class' : 'form-control'}),
            'name' : forms.TextInput(attrs={'class': 'form-control', 'required':'required', 'placeholder':'Item/Product/Service Name'}),
            'slug' : forms.TextInput(attrs={'class': 'form-control','readonly': 'readonly'}),
            'description' : forms.Textarea(attrs={'class': 'form-control', 'required': 'required', 'rows': 4, 'placeholder':'Item/Product/Service Description'}),
            'category' : forms.Select(attrs={'class': 'form-select select2', 'required': 'required'}),
            'unit_type' : forms.TextInput(attrs={'class': 'form-control', 'required': 'required','placeholder':'Unit type (eg. Item, Hours, Pcs, etc.)'}),
            'rate' : forms.NumberInput(attrs={'class': 'form-control', 'required': 'required', 'placeholder':'Item/Product/Service Price'}),
            'fake_sales' : forms.NumberInput(attrs={'class': 'form-control', 'placeholder':'Sales count'}),
            'fake_stars' : forms.NumberInput(attrs={'class': 'form-control', 'placeholder':'Max 5 starts'}),
        }
        
class ItemSelectionForm(forms.Form):
    selected_item = forms.ModelChoiceField(
        queryset=items.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'yourSelectInput'}),
    )
    quantity = forms.IntegerField(
        min_value=1,
        initial=1,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
    )

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')

        if quantity is None:
            return 1

        return quantity


    
# Item Category Form
class CRMItemCategoryForm(forms.ModelForm):
    class Meta:
        model = itemCategory
        fields = '__all__'
        widgets = {
            'name' : forms.TextInput(attrs={'class': 'form-control', 'required': 'required', 'placeholder':'Name' }),
            'slug' : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Slug', 'readonly': 'readonly'}),
        }

# CRM Project Form
class CRMProjectsForm(forms.ModelForm):
    class Meta:
        model = crmProjects
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}),
            'progress' : forms.NumberInput(attrs={'class' : 'form-control' , 'placeholder' : 'Enter between 1 - 100', 'max': 100}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Read only', 'readonly': 'readonly'}),
            'project_type': forms.Select(attrs={'class': 'form-select select2'}),
            'client': forms.Select(attrs={'class': 'form-select select2'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description', 'rows':4}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type':'date', 'placeholder': 'Start Date'}),
            'deadline': forms.DateInput(attrs={'class': 'form-control','type':'date', 'placeholder': 'Deadline'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Price'}),
            'label': forms.Select(attrs={'class': 'form-select select2'}),
            'team' : forms.SelectMultiple(attrs={'class': 'form-select', 'id' : 'multiple-select-field', 'data-placeholder' : 'Choose anything', 'multiple' : 'multiple'}),
        }

# CRM Client Form
class CRMClientForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ('profile_picture', 'name', 'slug', 'email', 'phone', 'address', 'city', 'state', 'country', 'zipcode', 'facebook', 'instagram', 'linkedin')
        widgets = {
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
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
            user.save()
            instance.save()
        return instance

# CRM Task Form
class CRMTaskForm(forms.ModelForm):
    class Meta:
        model = crmTasks
        fields = '__all__'
        exclude = ['project']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter task title'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Read only', 'readonly': 'readonly'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter task description', 'rows': 4}),
            'status': forms.Select(attrs={'class': 'form-select', 'id': 'task-status'}),
            'priority': forms.Select(attrs={'class': 'form-select', 'id': 'task-priority'}),
            'label': forms.Select(attrs={'class': 'form-select', 'id': 'task-label'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'deadline': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'assigned_to' : forms.SelectMultiple(attrs={'class': 'form-select', 'id' : 'multiple-select-field', 'data-placeholder' : 'Choose anything', 'multiple' : 'multiple'}),
        }

# Invoice Form
class invoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['title','number','number','status','billDate','dueDate','notes', 'project']
        widgets = {
            'title' : forms.TextInput(attrs={'class' : 'form-control'}),
            'number' : forms.TextInput(attrs={'class' : 'form-control', 'readonly':'readonly'}),
            'notes' : forms.Textarea(attrs={'class' : 'form-control', 'rows':4}),
            'status' : forms.Select(attrs={'class':'form-select'}),
            'billDate' : forms.DateInput(attrs={'class':'form-control', 'type':'date'}),
            'dueDate' : forms.DateInput(attrs={'class':'form-control', 'type':'date'}),
            'project' : forms.Select(attrs={'class':'form-select select2'}),
        }

class discountForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['discount_amount']
        widgets = {
            'discount_amount' : forms.NumberInput(attrs={'class' : 'form-control'}),
        }

class taxForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['tax_amount']
        widgets = {
            'tax_amount' : forms.NumberInput(attrs={'class' : 'form-control'}),
        }

class otherFeeForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['other_fees_name' ,'other_fees_amount']
        widgets = {
            'other_fees_name' : forms.TextInput(attrs={'class' : 'form-control'}),
            'other_fees_amount' : forms.NumberInput(attrs={'class' : 'form-control'}),
        }

class ClientSelectForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        self.initial_client = kwargs.pop('initial_client', None)
        self.CLIENT_LIST = User.objects.filter(role=User.Role.Guser)
        self.CLIENT_CHOICES = []

        self.CLIENT_CHOICES.append(('', '---Select Client---'))
        for client in self.CLIENT_LIST:
            d_t = (client.id, client.username)  # using the user's id and username for the choices
            self.CLIENT_CHOICES.append(d_t)

        super(ClientSelectForm,self).__init__(*args,**kwargs)

        self.fields['client'] = forms.ChoiceField(
                                        label='Choose a related client',
                                        choices = self.CLIENT_CHOICES,
                                        widget=forms.Select(attrs={'class': 'form-select mb-3 select2'}),)

    class Meta:
        model = Invoice
        fields = ['client']

    def clean_client(self):
        c_client = self.cleaned_data['client']
        if c_client == '':
            return self.initial_client
        else:
            return User.objects.get(id=c_client)
        
# Payment Form
class PaymentsForm(forms.ModelForm):
    class Meta:
        model = Payments
        fields = '__all__'
        widgets = {
            'invoice': forms.Select(attrs={'class': 'form-select select2', 'required': 'required'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title', 'required': 'required'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Read only', 'readonly': 'readonly'}),
            'payment_method': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Payment Method', 'required': 'required'}),
            'transaction_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Transaction ID'}),
            'payment_ammount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Payment Amount', 'required': 'required'}),
            'payment_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'Payment Date', 'required': 'required'}),
            'payment_note': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Payment Note', 'rows': 1}),
        }

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = '__all__'
        widgets = {
            'date_of_expense': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'Date of Expense'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}),
            'amount' : forms.NumberInput(attrs={'class' : 'form-control', 'placeholder' : 'Expense Amount'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Read only', 'readonly': 'readonly'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description', 'rows': 4}),
        }
