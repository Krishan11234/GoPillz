from django.db import models
from django.contrib.auth.models import User
from .helper import PLAN_CHOICES, DURATION_CHOICES


class Plan(models.Model):
    plan_type = models.CharField(max_length=255, null=True, db_index=True, choices=PLAN_CHOICES)
    price = models.IntegerField(blank=True, default=0)
    duration = models.CharField(max_length=100, null=True, db_index=True, choices=DURATION_CHOICES)


class PaymentMethod(models.Model):
    method_name = models.CharField(max_length=150)
    upload = models.FileField(upload_to='paymentlogo')


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_status = models.CharField(max_length=100)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    expired = models.BooleanField(blank=False)
    renew = models.BooleanField(blank=False, null=True, default=False)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE)
    created = models.DateTimeField(blank=True, null=True)
    exp_date = models.DateTimeField(blank=True, null=True)


class SubscriberCount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_subscriber_count = models.IntegerField(blank=True, default=0)
    used_subscriber_count = models.IntegerField(blank=True, default=0)


