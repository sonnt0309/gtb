from django.contrib import admin
from .models import Activation
from advanced_filters.admin import AdminAdvancedFiltersMixin
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from django.core.paginator import EmptyPage, InvalidPage, Paginator
from django.contrib.admin.views.main import ChangeList
from helper.CategoryChoiceField import UserFullnameChoiceField
from django.contrib import messages


# Register your models here.
class InlineChangeList(object):
    can_show_all = True
    multi_page = True
    get_query_string = ChangeList.__dict__['get_query_string']

    def __init__(self, request, page_num, paginator):
        self.show_all = 'all' in request.GET
        self.page_num = page_num
        self.paginator = paginator
        self.result_count = paginator.count
        self.params = dict(request.GET.items())


class ActivationAdmin(AdminAdvancedFiltersMixin, admin.ModelAdmin):
    change_form_template = 'admin/custom/change_form_key.html'
    list_display = (
        'activate_key', 'get_username', 'get_full_name_kanji', 'get_license', 'activate_date_time', 'pc_name',
        'windows_product_id', 'mac_address', 'drive_serial_number', 'activate_status_code')
    list_display_links = ('activate_key', 'get_license')
    advanced_filter_fields = (
        'activate_key',
        ('license__user__username', _('user')),
        ('license__user__profile__full_name_kanji', _('full name')),
        ('license__license_key', _('License ID')),
        'activate_date_time',
        'pc_name',
        'windows_product_id',
        'mac_address',
        'drive_serial_number',
        'activate_status_code',
        'created_date',
        'updated_date',
    )
    fields = ('activate_key', 'license', 'activate_date_time', 'pc_name', 'windows_product_id', 'mac_address',
              'drive_serial_number', 'activate_status_code', 'created_date', 'updated_date')
    readonly_fields = ('created_date', 'updated_date')
    # hidden fields
    exclude = ('is_deleted',)
    # per_page pagination
    list_per_page = settings.LIST_PER_PAGE

    def get_username(self, obj):
        return mark_safe(
            """<a href='/admin/user/user/%s/change'>%s</a>""" % (obj.license.user.id, obj.license.user.username))

    def get_full_name_kanji(self, obj):
        return obj.license.user.profile.full_name_kanji

    def get_license(self, obj):
        return mark_safe(
            """<a href='/admin/license/license/%s/change'>%s</a>""" % (obj.license.id, obj.license.license_key))

    def get_form(self, request, obj=None, **kwargs):
        form = super(ActivationAdmin, self).get_form(request, obj, **kwargs)
        try:
            if self.has_change_permission(request):
                form.base_fields['license'].widget.can_change_related = False
            if self.has_add_permission(request):
                form.base_fields['license'].widget.can_add_related = False
        except (KeyError, TypeError) as e:
            print('Error get_form CustomActivation: %s' % e)
            messages.error(request, _(
                'An unexpected error has occurred. Please contact your system administrator. ') + 'Error get_form ActivationAdmin: %s' % e)
        return form

    # title
    get_username.short_description = _('user')
    get_full_name_kanji.short_description = _('full name')
    get_license.short_description = _('License ID')
    # sort
    get_username.admin_order_field = 'license__user__username'
    get_full_name_kanji.admin_order_field = 'license__user__profile__full_name_kanji'
    get_license.admin_order_field = 'license__license_key'


admin.site.register(Activation, ActivationAdmin)
