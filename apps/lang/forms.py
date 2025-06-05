from django import forms
from apps.lang.models import Languages

class LanguageForm(forms.ModelForm):
    class Meta:
        model = Languages
        fields = '__all__'
        widgets = {
            'is_rtl': forms.CheckboxInput(attrs={'class': 'form-check-input', 'type': 'checkbox', 'id': 'rtlSwitch'}),
            'is_default': forms.CheckboxInput(attrs={'class': 'form-check-input', 'type': 'checkbox', 'id': 'defaultSwitch'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'