from django.contrib import admin
from .models import *


class PlanAdmin(admin.ModelAdmin):
    fieldsets = ()
    list_display = ('plan_type', 'price', 'duration',)
    # search_fields = ('rule_name',)
    model = Plan


class PaymentMethodAdmin(admin.ModelAdmin):
    fieldsets = ()
    list_display = ('method_name',)
    search_fields = ('rule_name',)
    model = PaymentMethod


admin.site.register(Plan, PlanAdmin)
admin.site.register(PaymentMethod, PaymentMethodAdmin)
