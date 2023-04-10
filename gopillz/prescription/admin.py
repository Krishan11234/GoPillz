from django.contrib import admin
from .models import *


class MedicineAdmin(admin.ModelAdmin):
    fieldsets = ()
    list_display = ('medicine_name', 'medicine_type', 'schedule_time', 'datetime', 'level_of_engagement')
    model = Medicine


class PrescriptionAdmin(admin.ModelAdmin):
    fieldsets = ()
    list_display = ('user',)
    model = Medicine


class EmailVerificationAdmin(admin.ModelAdmin):
    fieldsets = ()
    list_display = ('user', 'email', 'verified')
    model = Medicine


admin.site.register(Medicine, MedicineAdmin)
admin.site.register(Doctor)
admin.site.register(Caregiver)
admin.site.register(Prescription, PrescriptionAdmin)
admin.site.register(PrescriptionFiles)
admin.site.register(EmailVerification, EmailVerificationAdmin)
admin.site.register(Subscriber)
