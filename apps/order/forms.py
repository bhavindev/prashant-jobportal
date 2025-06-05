from django import forms 
from apps.order.models import Order, PromoCode

# Order status form
class orderStatusForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-select select2'
        
# Promo Code Form
class promoCodeForm(forms.ModelForm):
    class Meta:
        model = PromoCode
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'