from django import forms
from .models import  Category, Reservation


PAYMENT_CHOICES = (
    ('STRIPE', 'STRIPE'),
    ('PAYPAL', 'PAYPAL')
)

class CheckOutForm(forms.Form):
    address = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'INPUT ADDRESS',
        'aria-label': 'Recipient\'s username',
        'aria-describedby': 'basic-addon2'
    }))
    phone = forms.IntegerField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'INPUT PHONE NUMBER',
        'aria-label': 'Recipient\'s username',
        'aria-describedby': 'basic-addon2'
    }))
    save_info = forms.BooleanField(widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))
    use_saved_info = forms.BooleanField(widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))

class CouponForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Promo code',
        'aria-label': 'Recipient\'s username',
        'aria-describedby': 'basic-addon2'
    }))









