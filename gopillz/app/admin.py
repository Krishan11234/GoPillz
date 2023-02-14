from django.contrib import admin
from .models import *
from prescription.models import *

# Register your models here.


class StaffAdminArea(admin.AdminSite):
    site_header = 'Staff Database'


class StaffAdminPermission(admin.ModelAdmin):
    list_display = ('subscriber_name', 'phone_number', 'address', 'city', 'country', 'pin_code')
    model = Subscriber
    # fieldsets = (
    #     (
    #         'Basic', {
    #             'fields': (
    #                 'subscriber_name'
    #             )
    #         }
    #     ),
    # )

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
        query = super(StaffAdminPermission, self).get_queryset(request)
        filtered_query = query.filter(added_by=request.user)
        return filtered_query


staff_site = StaffAdminArea(name='StaffAdmin')
staff_site.register(Subscriber, StaffAdminPermission)

admin.site.register(ContactUs)
admin.site.register(Profile)