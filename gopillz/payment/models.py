from django.db import models

DURATION_CHOICES = (
    ("yearly", "yearly"),
    ("monthly", "monthly"),
)

PLAN_CHOICES = (
    ("couple", "Couple"),
    ("single", "Single"),
    ("family_friends", "Family & Friends"),
)


class Plan(models.Model):
    plan_type = models.CharField(max_length=255, null=True, db_index=True, choices=PLAN_CHOICES)
    price = models.IntegerField(blank=True, default=0)
    duration = models.CharField(max_length=100, null=True, db_index=True, choices=DURATION_CHOICES)


class PaymentMethod(models.Model):
    method_name = models.CharField(max_length=150)
    upload = models.FileField(upload_to='paymentlogo')
