from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from .helper import MEDICINE_TYPE, NUMBER_DAYS, SCHEDULE_TIME, LEVEL_ENGAGEMENT


class Subscriber(models.Model):
    subscriber_name = models.CharField(max_length=100)


class Medicine(models.Model):
    medicine_name = models.CharField(max_length=100)
    medicine_type = models.CharField(max_length=100, null=True, db_index=True, choices=MEDICINE_TYPE)
    number_days = models.CharField(max_length=100, null=True, db_index=True, choices=NUMBER_DAYS)
    schedule_time = models.CharField(max_length=100, null=True, db_index=True, choices=SCHEDULE_TIME)
    level_of_engagement = models.CharField(max_length=100, null=True, db_index=True, choices=LEVEL_ENGAGEMENT)


class Doctor(models.Model):
    doctor_name = models.CharField(max_length=100)
    doctor_phone_no = PhoneNumberField(null=False, blank=False, unique=True)
    city = models.CharField(max_length=100)
    hospital_name = models.CharField(max_length=100)
    Ailment = models.CharField(max_length=100)


class Caregiver(models.Model):
    caregiver_name = models.CharField(max_length=100)
    phone_no = PhoneNumberField(null=False, blank=False, unique=True)
    email = models.EmailField(max_length=255)
    relation = models.CharField(max_length=255)


class Prescription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    upload_prescription = models.FileField(upload_to='prescription/', blank=True, null=True)
    medicine = models.ForeignKey(Medicine, blank=True, null=True, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, blank=True, null=True, on_delete=models.CASCADE)
    caregiver = models.ForeignKey(Caregiver, blank=True, null=True, on_delete=models.CASCADE)
    subscriber = models.ManyToManyField(Subscriber, blank=True, null=True)



