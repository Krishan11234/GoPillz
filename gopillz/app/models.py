from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp = models.BigIntegerField()
    expired = models.BooleanField(blank=False)
    phone_user = models.CharField(max_length=100, blank=True)
    password = models.CharField(max_length=100, blank=True)
    user_name = models.CharField(max_length=100, blank=True)


class ContactUs(models.Model):
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_no = PhoneNumberField(null=False, blank=False, unique=True)
    message = models.TextField(blank=True, null=True)