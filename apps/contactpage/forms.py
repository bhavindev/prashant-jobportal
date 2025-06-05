from django import forms
from apps.contactpage.models import Subscriber
from ckeditor.widgets import CKEditorWidget

class SubscriberForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ['email']
        
class EmailSelectForm(forms.ModelForm):
    select_all = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    subscribers = forms.ModelMultipleChoiceField(
        queryset=Subscriber.objects.all(),
        widget=forms.SelectMultiple(),
        required=False
    )
    subject = forms.CharField(max_length=200, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    message = forms.CharField(widget=CKEditorWidget())
    manually_added_emails = forms.CharField(
        label="Manually Add Emails (comma-separated)",
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder' : 'email1@gmail.com,email2@gmail.com,email3@gmail.com', 'rows' : 3})
    )

    class Meta:
        model = Subscriber
        fields = ['select_all', 'subscribers', 'manually_added_emails', 'subject', 'message']
