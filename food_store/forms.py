from django import forms
from .models import  Category, Reservation
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberInternationalFallbackWidget, PhoneNumberPrefixWidget


PAYMENT_CHOICES = (
    ('STRIPE', 'STRIPE'),
    ('PAYPAL', 'PAYPAL')
)

class CheckOutForm(forms.Form):
    address = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'INPUT ADDRESS',
        'aria-label': 'Recipient\'s username',
        'aria-describedby': 'basic-addon2'
    }))
    phone = PhoneNumberField(required=False, widget=PhoneNumberPrefixWidget(attrs={
        'class': 'form-control',
        'placeholder': 'INPUT PHONE NUMBER',
        'aria-describedby': 'basic-addon2'
    }))
    save_info = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={
        'class': 'form-control',
        'id': 'save_checkbox'
    }))
    use_saved_info = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={
        'class': 'form-control',
        'id': 'fetch_checkbox'
    }))

class CouponForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Promo code',
        'aria-label': 'Recipient\'s username',
        'aria-describedby': 'basic-addon2'
    }))









