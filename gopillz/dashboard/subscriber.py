from django.contrib import admin
from prescription.models import Subscriber
from django.core.exceptions import ValidationError
from django.contrib import messages
# Register your models here.


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
        messages.add_message(request, messages.WARNING, (
            'Failed'
        ))


staff_site = UserAdminArea(name='UserDashboard')
staff_site.register(Subscriber, UserAdminPermission)
