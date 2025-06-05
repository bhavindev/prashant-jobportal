from django import forms 
from apps.custompage.models import customPage

class customPageForm(forms.ModelForm):
    class Meta:
        model = customPage
        fields = '__all__'
        exclude = ['language']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control' 