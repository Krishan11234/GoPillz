from django.contrib import admin
from prescription.models import Subscriber
from django.core.exceptions import ValidationError
from django.contrib import messages
from .models import *
# Register your models here.
# from .forms import PaymentLinkForm


class UserAdminArea(admin.AdminSite):
    site_header = 'User Dashboard'


class UserAdminPermission(admin.ModelAdmin):
    list_display = ('subscriber_name', 'phone_number', 'address', 'city', 'country', 'pin_code')
    model = Subscriber


    fieldsets = (
        (
            'SUBSCRIBER INFORMATION', {
             'fields': (
                ('subscriber_name',),
                ('phone_number',),
                ('address',),
                ('city',),
                ('country',),
                ('pin_code',),
             ),
            }
        ),
    )

    def has_module_permission(self, request):
        return True

    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        return False

    def has_view_permission(self, request, obj=None):
        return obj is None or obj.added_by == request.user

    def has_delete_permission(self, request, obj=None):
        return False

    def get_queryset(self, request):
        query = super(UserAdminPermission, self).get_queryset(request)
        filtered_query = query.filter(added_by=request.user)
        return filtered_query

    def save_model(self, request, obj, form, change):
        # if request.POST.get('action') == 'add_selected':
        #     pass
        #
        # if getattr(obj, 'author', None) is None:
        #     obj.added_by = request.user
        # obj.save()
        storage = messages.get_messages(request)
        storage.used = True
        # messages.add_message(request, messages.WARNING, 'Failed')
        # print('------------------')


# @admin.register(Subscriber)
# class MyModelAdmin(admin.ModelAdmin):
#     # Here
#     def save_model(self, request, obj, form, change):
#         # obj.save()
#         messages.add_message(request, messages.INFO, 'Custom Message')


staff_site = UserAdminArea(name='UserDashboard')
staff_site.register(Subscriber, UserAdminPermission)


class PatientAdminPermission(admin.ModelAdmin):
    model = Patient

    fieldsets = (
        (
            'PATIENT INFORMATION', {
                'fields': (
                    ('name',),
                    ('phone_number',),
                ),
            }
        ),
    )

    def has_module_permission(self, request):
        return True

    def has_add_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_view_permission(self, request, obj=None):
        return obj is None or obj.user == request.user

    def has_delete_permission(self, request, obj=None):
        return True

    def get_queryset(self, request):
        query = super(PatientAdminPermission, self).get_queryset(request)
        filtered_query = query.filter(user=request.user)
        return filtered_query

    def save_model(self, request, obj, form, change):
        patient_data = Patient.objects.filter(user=request.user)
        if not patient_data:
            if getattr(obj, 'author', None) is None:
                obj.user = request.user
                obj.save()
        else:
            messages.add_message(request, messages.WARNING, 'Can not add more')


class FamilyMemberAdminPermission(admin.ModelAdmin):
    model = FamilyMember
    fieldsets = (
        (
            'Family Member INFORMATION', {
                'fields': (
                    ('patient_fam',),
                    ('fam_name',),
                    ('fam_number',),
                ),
            }
        ),
    )

    def has_module_permission(self, request):
        return True

    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_view_permission(self, request, obj=None):
        return obj is None or obj.user == request.user

    def has_delete_permission(self, request, obj=None):
        return True

    def get_queryset(self, request):
        query = super(FamilyMemberAdminPermission, self).get_queryset(request)
        filtered_query = query.filter(user=request.user)
        return filtered_query

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'author', None) is None:
            obj.user = request.user
            obj.save()


staff_site.register(User)
staff_site.register(Patient, PatientAdminPermission)

staff_site.register(FamilyMember, FamilyMemberAdminPermission)


class DoctorAdminPermission(admin.ModelAdmin):
    model = Doctor
    fieldsets = (
        (
            'Doctor INFORMATION', {
                'fields': (
                    ('doctor_name',),
                    ('doctor_email',),
                    ('speciality',),
                ),
            }
        ),
    )

    def has_module_permission(self, request):
        return True

    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_view_permission(self, request, obj=None):
        return obj is None or obj.user == request.user

    def has_delete_permission(self, request, obj=None):
        return True

    def get_queryset(self, request):
        query = super(DoctorAdminPermission, self).get_queryset(request)
        filtered_query = query.filter(user=request.user)
        return filtered_query

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'author', None) is None:
            obj.user = request.user
            obj.save()


staff_site.register(Doctor, DoctorAdminPermission)


class DoctorPatientAdminPermission(admin.ModelAdmin):
    model = DoctorPatient

    # fieldsets = (
    #     (
    #         'PATIENT INFORMATION', {
    #             'fields': (
    #                 ('name',),
    #                 ('phone_number',),
    #             ),
    #         }
    #     ),
    # )
    def has_module_permission(self, request):
        return True

    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_view_permission(self, request, obj=None):
        return True

    def get_queryset(self, request):
        query = super(DoctorPatientAdminPermission, self).get_queryset(request)
        patient_info = Patient.objects.filter(user=request.user)
        filtered_query = query.filter(patient_doc=patient_info[0])
        return filtered_query

    # def save_model(self, request, obj, form, change):
    #     if getattr(obj, 'author', None) is None:
    #         obj.user = request.user
    #         obj.save()

    def has_delete_permission(self, request, obj=None):
        return True


staff_site.register(DoctorPatient, DoctorPatientAdminPermission)


class DoctorPhoneNumbersAdminPermission(admin.ModelAdmin):
    model = DoctorPatient

    # fieldsets = (
    #     (
    #         'PATIENT INFORMATION', {
    #             'fields': (
    #                 ('name',),
    #                 ('phone_number',),
    #             ),
    #         }
    #     ),
    # )
    def has_module_permission(self, request):
        return True

    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_view_permission(self, request, obj=None):
        return True

    # def get_queryset(self, request):
    #     query = super(DoctorPhoneNumbersAdminPermission, self).get_queryset(request)
    #     patient_info = Patient.objects.filter(user=request.user)
    #     filtered_query = query.filter(patient_doc=patient_info[0])
    #     return filtered_query

    # def save_model(self, request, obj, form, change):
    #     if getattr(obj, 'author', None) is None:
    #         obj.user = request.user
    #         obj.save()

    def has_delete_permission(self, request, obj=None):
        return True


staff_site.register(DoctorPhoneNumbers, DoctorPhoneNumbersAdminPermission)


class AmbulanceAdminPermission(admin.ModelAdmin):
    model = DoctorPatient

    # fieldsets = (
    #     (
    #         'PATIENT INFORMATION', {
    #             'fields': (
    #                 ('name',),
    #                 ('phone_number',),
    #             ),
    #         }
    #     ),
    # )
    def has_module_permission(self, request):
        return True

    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_view_permission(self, request, obj=None):
        return True

    # def get_queryset(self, request):
    #     query = super(DoctorPhoneNumbersAdminPermission, self).get_queryset(request)
    #     patient_info = Patient.objects.filter(user=request.user)
    #     filtered_query = query.filter(patient_doc=patient_info[0])
    #     return filtered_query

    # def save_model(self, request, obj, form, change):
    #     if getattr(obj, 'author', None) is None:
    #         obj.user = request.user
    #         obj.save()

    def has_delete_permission(self, request, obj=None):
        return True


staff_site.register(Ambulance, AmbulanceAdminPermission)


class AmbulancePatientAdminPermission(admin.ModelAdmin):
    model = DoctorPatient

    # fieldsets = (
    #     (
    #         'PATIENT INFORMATION', {
    #             'fields': (
    #                 ('name',),
    #                 ('phone_number',),
    #             ),
    #         }
    #     ),
    # )
    def has_module_permission(self, request):
        return True

    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_view_permission(self, request, obj=None):
        return True

    # def get_queryset(self, request):
    #     query = super(DoctorPhoneNumbersAdminPermission, self).get_queryset(request)
    #     patient_info = Patient.objects.filter(user=request.user)
    #     filtered_query = query.filter(patient_doc=patient_info[0])
    #     return filtered_query

    # def save_model(self, request, obj, form, change):
    #     if getattr(obj, 'author', None) is None:
    #         obj.user = request.user
    #         obj.save()

    def has_delete_permission(self, request, obj=None):
        return True


staff_site.register(AmbulancePatient,AmbulancePatientAdminPermission)


class AmbulancePhoneNumbersAdminPermission(admin.ModelAdmin):
    model = DoctorPatient

    # fieldsets = (
    #     (
    #         'PATIENT INFORMATION', {
    #             'fields': (
    #                 ('name',),
    #                 ('phone_number',),
    #             ),
    #         }
    #     ),
    # )
    def has_module_permission(self, request):
        return True

    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_view_permission(self, request, obj=None):
        return True

    # def get_queryset(self, request):
    #     query = super(DoctorPhoneNumbersAdminPermission, self).get_queryset(request)
    #     patient_info = Patient.objects.filter(user=request.user)
    #     filtered_query = query.filter(patient_doc=patient_info[0])
    #     return filtered_query

    # def save_model(self, request, obj, form, change):
    #     if getattr(obj, 'author', None) is None:
    #         obj.user = request.user
    #         obj.save()

    def has_delete_permission(self, request, obj=None):
        return True


staff_site.register(AmbulancePhoneNumbers,AmbulancePhoneNumbersAdminPermission)


class LabAdminPermission(admin.ModelAdmin):
    model = DoctorPatient

    # fieldsets = (
    #     (
    #         'PATIENT INFORMATION', {
    #             'fields': (
    #                 ('name',),
    #                 ('phone_number',),
    #             ),
    #         }
    #     ),
    # )
    def has_module_permission(self, request):
        return True

    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_view_permission(self, request, obj=None):
        return True

    # def get_queryset(self, request):
    #     query = super(DoctorPhoneNumbersAdminPermission, self).get_queryset(request)
    #     patient_info = Patient.objects.filter(user=request.user)
    #     filtered_query = query.filter(patient_doc=patient_info[0])
    #     return filtered_query

    # def save_model(self, request, obj, form, change):
    #     if getattr(obj, 'author', None) is None:
    #         obj.user = request.user
    #         obj.save()

    def has_delete_permission(self, request, obj=None):
        return True


staff_site.register(Lab, LabAdminPermission)


class LabPatientAdminPermission(admin.ModelAdmin):
    model = DoctorPatient

    # fieldsets = (
    #     (
    #         'PATIENT INFORMATION', {
    #             'fields': (
    #                 ('name',),
    #                 ('phone_number',),
    #             ),
    #         }
    #     ),
    # )
    def has_module_permission(self, request):
        return True

    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_view_permission(self, request, obj=None):
        return True

    # def get_queryset(self, request):
    #     query = super(DoctorPhoneNumbersAdminPermission, self).get_queryset(request)
    #     patient_info = Patient.objects.filter(user=request.user)
    #     filtered_query = query.filter(patient_doc=patient_info[0])
    #     return filtered_query

    # def save_model(self, request, obj, form, change):
    #     if getattr(obj, 'author', None) is None:
    #         obj.user = request.user
    #         obj.save()

    def has_delete_permission(self, request, obj=None):
        return True


staff_site.register(LabPatient, LabPatientAdminPermission)


class LabPhoneNumbersAdminPermission(admin.ModelAdmin):
    model = DoctorPatient

    # fieldsets = (
    #     (
    #         'PATIENT INFORMATION', {
    #             'fields': (
    #                 ('name',),
    #                 ('phone_number',),
    #             ),
    #         }
    #     ),
    # )
    def has_module_permission(self, request):
        return True

    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_view_permission(self, request, obj=None):
        return True

    # def get_queryset(self, request):
    #     query = super(DoctorPhoneNumbersAdminPermission, self).get_queryset(request)
    #     patient_info = Patient.objects.filter(user=request.user)
    #     filtered_query = query.filter(patient_doc=patient_info[0])
    #     return filtered_query

    # def save_model(self, request, obj, form, change):
    #     if getattr(obj, 'author', None) is None:
    #         obj.user = request.user
    #         obj.save()

    def has_delete_permission(self, request, obj=None):
        return True


staff_site.register(LabPhoneNumbers,LabPhoneNumbersAdminPermission)


class ChemistAdminPermission(admin.ModelAdmin):
    model = DoctorPatient

    # fieldsets = (
    #     (
    #         'PATIENT INFORMATION', {
    #             'fields': (
    #                 ('name',),
    #                 ('phone_number',),
    #             ),
    #         }
    #     ),
    # )
    def has_module_permission(self, request):
        return True

    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_view_permission(self, request, obj=None):
        return True

    # def get_queryset(self, request):
    #     query = super(DoctorPhoneNumbersAdminPermission, self).get_queryset(request)
    #     patient_info = Patient.objects.filter(user=request.user)
    #     filtered_query = query.filter(patient_doc=patient_info[0])
    #     return filtered_query

    # def save_model(self, request, obj, form, change):
    #     if getattr(obj, 'author', None) is None:
    #         obj.user = request.user
    #         obj.save()

    def has_delete_permission(self, request, obj=None):
        return True


staff_site.register(Chemist, ChemistAdminPermission)


class ChemistPatientAdminPermission(admin.ModelAdmin):
    model = DoctorPatient

    # fieldsets = (
    #     (
    #         'PATIENT INFORMATION', {
    #             'fields': (
    #                 ('name',),
    #                 ('phone_number',),
    #             ),
    #         }
    #     ),
    # )
    def has_module_permission(self, request):
        return True

    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_view_permission(self, request, obj=None):
        return True

    # def get_queryset(self, request):
    #     query = super(DoctorPhoneNumbersAdminPermission, self).get_queryset(request)
    #     patient_info = Patient.objects.filter(user=request.user)
    #     filtered_query = query.filter(patient_doc=patient_info[0])
    #     return filtered_query

    # def save_model(self, request, obj, form, change):
    #     if getattr(obj, 'author', None) is None:
    #         obj.user = request.user
    #         obj.save()

    def has_delete_permission(self, request, obj=None):
        return True


staff_site.register(ChemistPatient,ChemistPatientAdminPermission)


class ChemistPhoneNumbersAdminPermission(admin.ModelAdmin):
    model = DoctorPatient

    # fieldsets = (
    #     (
    #         'PATIENT INFORMATION', {
    #             'fields': (
    #                 ('name',),
    #                 ('phone_number',),
    #             ),
    #         }
    #     ),
    # )
    def has_module_permission(self, request):
        return True

    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_view_permission(self, request, obj=None):
        return True

    # def get_queryset(self, request):
    #     query = super(DoctorPhoneNumbersAdminPermission, self).get_queryset(request)
    #     patient_info = Patient.objects.filter(user=request.user)
    #     filtered_query = query.filter(patient_doc=patient_info[0])
    #     return filtered_query

    # def save_model(self, request, obj, form, change):
    #     if getattr(obj, 'author', None) is None:
    #         obj.user = request.user
    #         obj.save()

    def has_delete_permission(self, request, obj=None):
        return True


staff_site.register(ChemistPhoneNumbers,ChemistPhoneNumbersAdminPermission)


class DosesAdminPermission(admin.ModelAdmin):
    model = DoctorPatient

    # fieldsets = (
    #     (
    #         'PATIENT INFORMATION', {
    #             'fields': (
    #                 ('name',),
    #                 ('phone_number',),
    #             ),
    #         }
    #     ),
    # )
    def has_module_permission(self, request):
        return True

    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_view_permission(self, request, obj=None):
        return True

    # def get_queryset(self, request):
    #     query = super(DoctorPhoneNumbersAdminPermission, self).get_queryset(request)
    #     patient_info = Patient.objects.filter(user=request.user)
    #     filtered_query = query.filter(patient_doc=patient_info[0])
    #     return filtered_query

    # def save_model(self, request, obj, form, change):
    #     if getattr(obj, 'author', None) is None:
    #         obj.user = request.user
    #         obj.save()

    def has_delete_permission(self, request, obj=None):
        return True


staff_site.register(Doses,DosesAdminPermission)


class MedicineAdminPermission(admin.ModelAdmin):
    model = DoctorPatient

    # fieldsets = (
    #     (
    #         'PATIENT INFORMATION', {
    #             'fields': (
    #                 ('name',),
    #                 ('phone_number',),
    #             ),
    #         }
    #     ),
    # )
    def has_module_permission(self, request):
        return True

    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_view_permission(self, request, obj=None):
        return True

    # def get_queryset(self, request):
    #     query = super(DoctorPhoneNumbersAdminPermission, self).get_queryset(request)
    #     patient_info = Patient.objects.filter(user=request.user)
    #     filtered_query = query.filter(patient_doc=patient_info[0])
    #     return filtered_query

    # def save_model(self, request, obj, form, change):
    #     if getattr(obj, 'author', None) is None:
    #         obj.user = request.user
    #         obj.save()

    def has_delete_permission(self, request, obj=None):
        return True


staff_site.register(Medicine, MedicineAdminPermission)


class MedicineDayAdminPermission(admin.ModelAdmin):
    model = DoctorPatient

    # fieldsets = (
    #     (
    #         'PATIENT INFORMATION', {
    #             'fields': (
    #                 ('name',),
    #                 ('phone_number',),
    #             ),
    #         }
    #     ),
    # )
    def has_module_permission(self, request):
        return True

    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_view_permission(self, request, obj=None):
        return True

    # def get_queryset(self, request):
    #     query = super(DoctorPhoneNumbersAdminPermission, self).get_queryset(request)
    #     patient_info = Patient.objects.filter(user=request.user)
    #     filtered_query = query.filter(patient_doc=patient_info[0])
    #     return filtered_query

    # def save_model(self, request, obj, form, change):
    #     if getattr(obj, 'author', None) is None:
    #         obj.user = request.user
    #         obj.save()

    def has_delete_permission(self, request, obj=None):
        return True


staff_site.register(MedicineDay, MedicineDayAdminPermission)


class AilmentAdminPermission(admin.ModelAdmin):
    model = DoctorPatient

    # fieldsets = (
    #     (
    #         'PATIENT INFORMATION', {
    #             'fields': (
    #                 ('name',),
    #                 ('phone_number',),
    #             ),
    #         }
    #     ),
    # )
    def has_module_permission(self, request):
        return True

    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_view_permission(self, request, obj=None):
        return True

    # def get_queryset(self, request):
    #     query = super(DoctorPhoneNumbersAdminPermission, self).get_queryset(request)
    #     patient_info = Patient.objects.filter(user=request.user)
    #     filtered_query = query.filter(patient_doc=patient_info[0])
    #     return filtered_query

    # def save_model(self, request, obj, form, change):
    #     if getattr(obj, 'author', None) is None:
    #         obj.user = request.user
    #         obj.save()

    def has_delete_permission(self, request, obj=None):
        return True


staff_site.register(Ailment, AilmentAdminPermission)