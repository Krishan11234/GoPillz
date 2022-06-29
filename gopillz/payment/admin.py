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


class PaymentAdmin(admin.ModelAdmin):
    fieldsets = ()
    list_display = ('user', 'plan', 'payment_status', 'expired', 'renew', 'created')
    model = PaymentMethod


admin.site.register(Plan, PlanAdmin)
admin.site.register(PaymentMethod, PaymentMethodAdmin)
admin.site.register(Payment, PaymentAdmin)
