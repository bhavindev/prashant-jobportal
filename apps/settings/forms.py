from django import forms 
from apps.settings.models import websiteSetting, paymentMethod, PromotionalBanner

class openaiSettingsForm(forms.ModelForm):
    class Meta: 
        model = websiteSetting
        fields = ['openai_api', 'max_token', 'is_enabled_for_user']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            
class paymentMethodsForm(forms.ModelForm):
    class Meta:
        model = paymentMethod
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
        
class PromotionalBannerForm(forms.ModelForm):
    class Meta:
        model = PromotionalBanner
        fields = '__all__'
        widgets = {
            'promo_start_date': forms.TextInput(attrs={'class': 'form-control date-picker', 'id' : 'dpkr', 'type': 'date'}),
            'promo_end_date': forms.TextInput(attrs={'class': 'form-control date-picker', 'id' : 'dpkr2', 'type': 'date'}),
            'is_promo_active': forms.CheckboxInput(attrs={'class': 'form-check-input', 'type': 'checkbox', 'id': 'promoSwitch'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'