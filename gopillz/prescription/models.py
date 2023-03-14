from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from .helper import MEDICINE_TYPE, NUMBER_DAYS, SCHEDULE_TIME, LEVEL_ENGAGEMENT
from multiselectfield import MultiSelectField


class Subscriber(models.Model):
    subscriber_name = models.CharField(max_length=100)
    phone_number = PhoneNumberField(null=True, blank=False, unique=True)
    address = models.CharField(max_length=100, null=True, blank=False)
    city = models.CharField(max_length=100, null=True, blank=False)
    country = models.CharField(max_length=100, null=True, blank=False)
    pin_code = models.IntegerField(null=True, blank=False)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)


class Medicine(models.Model):
    medicine_name = models.CharField(max_length=100)
    medicine_type = models.CharField(max_length=100, null=True, db_index=True, choices=MEDICINE_TYPE)
    number_days = MultiSelectField(choices=NUMBER_DAYS, null=True)
    schedule_time = models.CharField(max_length=100, null=True, db_index=True)
    datetime = models.DateTimeField(null=True)
    level_of_engagement = models.CharField(max_length=100, null=True, db_index=True, choices=LEVEL_ENGAGEMENT)


class Days(models.Model):
    name = models.CharField(max_length=100)
    medicine_id = models.ForeignKey(Medicine, on_delete=models.CASCADE)


class Doctor(models.Model):
    doctor_name = models.CharField(max_length=100)
    doctor_phone_no = PhoneNumberField(null=True, blank=False, unique=True)
    city = models.CharField(max_length=100)
    hospital_name = models.CharField(max_length=100)
    Ailment = models.CharField(max_length=100)


class Caregiver(models.Model):
    caregiver_name = models.CharField(max_length=100)
    phone_no = PhoneNumberField(null=False, blank=False, unique=True)
    email = models.EmailField(max_length=255)
    relation = models.CharField(max_length=255)


class PrescriptionFiles(models.Model):
    name = models.FileField(upload_to='prescription/', blank=True, null=True)


class Prescription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    upload_prescription = models.ManyToManyField(PrescriptionFiles, blank=True)
    medicine = models.ForeignKey(Medicine, blank=True, null=True, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, blank=True, null=True, on_delete=models.CASCADE)
    caregiver = models.ForeignKey(Caregiver, blank=True, null=True, on_delete=models.CASCADE)
    subscriber = models.ManyToManyField(Subscriber, blank=True)


class EmailVerification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=254)
    verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=100, null=True, blank=False)
    rand_verification_string = models.CharField(max_length=250, null=True, blank=False)
    message_mail_sent = models.BooleanField(default=False)