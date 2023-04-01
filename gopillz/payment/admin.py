from django.contrib import admin
from .models import *
from .helper import PLAN_CHOICES


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
    list_display = ('user', 'plan_type', 'payment_method_name', 'payment_status', 'expired', 'renew', 'created')
    model = PaymentMethod

    def plan_type(self, obj):
        plan_type = obj.plan.plan_type
        for plan in PLAN_CHOICES:
            if plan[0] == plan_type:
                return plan[1]
        return plan_type

    def payment_method_name(self, obj):
        method_name = obj.payment_method.method_name
        return method_name


admin.site.register(Plan, PlanAdmin)
admin.site.register(PaymentMethod, PaymentMethodAdmin)
admin.site.register(Payment, PaymentAdmin)
