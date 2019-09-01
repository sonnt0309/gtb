from django.contrib import admin
from .models import ExecutionStatus
from advanced_filters.admin import AdminAdvancedFiltersMixin
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from helper.CategoryChoiceField import UserFullnameChoiceField
from django.contrib import messages


# Register your models here.
class ExecutionStatusAdmin(AdminAdvancedFiltersMixin, admin.ModelAdmin):
    change_form_template = 'admin/custom/change_form_key.html'
    list_display = (
        'app_exe_status_key', 'get_username', 'get_full_name_kanji', 'get_license', 'get_activation', 'get_pc_name',
        'get_windows_product_id', 'get_mac_address', 'get_drive_serial_number', 'start_app_datetime', 'status_last_update',
        'status_code', 'exe_status_expiration')
    advanced_filter_fields = (
        'app_exe_status_key',
        ('activation__license__user__username', _('user')),
        ('activation__license__user__profile__full_name_kanji', _('full name')),
        ('activation__license__license_key', _('License ID')),
        ('activation__activate_key', _('Activate ID')),
        ('activation__pc_name', _('pc name')),
        ('activation__windows_product_id', _('windows product ID')),
        ('activation__mac_address', _('mac address')),
        ('activation__drive_serial_number', _('drive serial number')),
        'start_app_datetime',
        'status_last_update',
        'status_code',
        'exe_status_expiration',
        'created_date',
        'updated_date',
    )
    fields = ('app_exe_status_key', 'activation', 'start_app_datetime', 'status_last_update', 'status_code',
              'exe_status_expiration', 'created_date', 'updated_date')
    readonly_fields = ('created_date', 'updated_date')
    # hidden fields
    exclude = ('is_deleted',)
    # per_page pagination
    list_per_page = settings.LIST_PER_PAGE

    def get_username(self, obj):
        return mark_safe("""<a href='/admin/user/user/%s/change'>%s</a>""" % (
        obj.activation.license.user.id, obj.activation.license.user.username))

    def get_full_name_kanji(self, obj):
        return obj.activation.license.user.profile.full_name_kanji

    def get_license(self, obj):
        return mark_safe("""<a href='/admin/license/license/%s/change'>%s</a>""" % (
        obj.activation.license.id, obj.activation.license.license_key))

    def get_activation(self, obj):
        return mark_safe("""<a href='/admin/activation/activation/%s/change'>%s</a>""" % (
        obj.activation.id, obj.activation.activate_key))

    def get_pc_name(self, obj):
        return obj.activation.pc_name

    def get_windows_product_id(self, obj):
        return obj.activation.windows_product_id

    def get_mac_address(self, obj):
        return obj.activation.mac_address

    def get_drive_serial_number(self, obj):
        return obj.activation.drive_serial_number

    def get_form(self, request, obj=None, **kwargs):
        form = super(ExecutionStatusAdmin, self).get_form(request, obj, **kwargs)
        try:
            if self.has_change_permission(request):
                form.base_fields['activation'].widget.can_change_related = False
            if self.has_add_permission(request):
                form.base_fields['activation'].widget.can_add_related = False
        except (KeyError, TypeError) as e:
            print('Error get_form ExecutionStatusAdmin: %s' % e)
            messages.error(request, _(
                'An unexpected error has occurred. Please contact your system administrator. ') + 'Error get_form ExecutionStatusAdmin: %s' % e)
        return form

    # title
    get_username.short_description = _('user')
    get_full_name_kanji.short_description = _('full name')
    get_license.short_description = _('License ID')
    get_activation.short_description = _('Activate ID')
    get_pc_name.short_description = _('pc name')
    get_windows_product_id.short_description = _('windows product ID')
    get_mac_address.short_description = _('mac address')
    get_drive_serial_number.short_description = _('drive serial number')
    # sort
    get_activation.admin_order_field = 'activation__activate_key'
    get_username.admin_order_field = 'activation__license__user__username'
    get_license.admin_order_field = 'activation__license__license_key'
    get_full_name_kanji.admin_order_field = 'activation__license__user__profile__full_name_kanji'
    get_pc_name.admin_order_field = 'activation__pc_name'
    get_windows_product_id.admin_order_field = 'activation__windows_product_id'
    get_mac_address.admin_order_field = 'activation__mac_address'
    get_drive_serial_number.admin_order_field = 'activation__drive_serial_number'


admin.site.register(ExecutionStatus, ExecutionStatusAdmin)

