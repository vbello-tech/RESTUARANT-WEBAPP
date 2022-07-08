from django import forms
from .models import Checkout, Category, Reservation


PAYMENT_CHOICES = (
    ('STRIPE', 'STRIPE'),
    ('PAYPAL', 'PAYPAL')
)

class CheckOutForm(forms.ModelForm):
    class Meta:
        model = Checkout
        fields = ('address', 'phone',)

        widgets = {
            'address': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    "placeholder": 'Enter your address',
                }
            ),
            'phone': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    "placeholder": 'Enter your address',
                }
            ),
        }

class CouponForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Promo code',
        'aria-label': 'Recipient\'s username',
        'aria-describedby': 'basic-addon2'
    }))









