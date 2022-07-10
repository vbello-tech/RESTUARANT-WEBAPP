from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone



class Userprofile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    phone = PhoneNumberField(blank=True, null=True)
    profile_pic = models.ImageField(upload_to="USER/", null=True, blank=True)
    bio = models.TextField(blank=True)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user}  profile"

class Checkout(models.Model):
    user = models.ForeignKey('auth.user', on_delete=models.CASCADE)
    address = models.CharField(max_length=1000, blank=False)
    phone = PhoneNumberField(blank=True, null=True)

    def __str__(self):
        return f"{self.user} ID: {self.user.id}"