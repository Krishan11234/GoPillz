from django.contrib import admin
from .models import *

admin.site.register(Subscriber)
admin.site.register(Medicine)
admin.site.register(Doctor)
admin.site.register(Caregiver)
admin.site.register(Prescription)
admin.site.register(PrescriptionFiles)
