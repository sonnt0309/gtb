from django.contrib import admin
from advanced_filters.admin import AdminAdvancedFiltersMixin
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from .models import License
from .models import LicenseOption
from django.utils.safestring import mark_safe
from django.contrib.admin.views.main import ChangeList
from django.core.paginator import EmptyPage, InvalidPage, Paginator
from helper.CategoryChoiceField import UserFullnameChoiceField, OptionChoiceField
from apps.admin.user.models import User
from apps.admin.option.models import Option
from django.contrib import messages
from apps.admin.activation.models import Activation


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


class ActivationInline(admin.TabularInline):
    model = Activation
    fields = ('get_activate_key',
              'get_user',
              'activate_date_time',
              'pc_name',
              'windows_product_id',
              'mac_address',
              'drive_serial_number',
              'activate_status_code',
              )
    readonly_fields = ('get_activate_key', 'get_user',)
    verbose_name_plural = _('activation')
    extra = 0

    def get_user(self, obj):
        return obj.license.user.profile.full_name_kanji

    def get_activate_key(self, obj):
        return mark_safe(
            """<a href='/admin/activation/activation/%s/change'>%s</a>""" % (obj.id, obj.activate_key))

    template = 'admin/edit_inline/tabular_paginated_custom.html'
    per_page = settings.LIST_PER_PAGE_INLINE

    get_activate_key.short_description = _('Activate ID')
    get_user.short_description = _('user')

    def get_formset(self, request, obj=None, **kwargs):
        formset_class = super(ActivationInline, self).get_formset(
            request, obj, **kwargs)

        class PaginationFormSet(formset_class):
            def __init__(self, *args, **kwargs):
                super(PaginationFormSet, self).__init__(*args, **kwargs)

                qs = self.queryset
                paginator = Paginator(qs, self.per_page)
                try:
                    page_num = int(request.GET.get('p', '0'))
                except ValueError:
                    page_num = 0

                try:
                    page = paginator.page(page_num + 1)
                except (EmptyPage, InvalidPage):
                    page = paginator.page(paginator.num_pages)

                self.cl = InlineChangeList(request, page_num, paginator)
                self.paginator = paginator

                if self.cl.show_all:
                    self._queryset = qs
                else:
                    self._queryset = page.object_list

        PaginationFormSet.per_page = self.per_page
        return PaginationFormSet


class LicenseOptionTabular(admin.TabularInline):
    model = LicenseOption
    fields = ('option', 'option_key', 'option_no', 'purchase_date',)
    readonly_fields = ('option_no', 'option_key',)
    verbose_name_plural = _('license options')
    extra = 0

    def option_no(self, obj):
        return obj.option.option_no

    def option_key(self, obj):
        return mark_safe(
            """<a href='/admin/option/option/%s/change'>%s</a>""" % (obj.option.id, obj.option.option_key))

    template = 'admin/edit_inline/tabular_paginated_custom.html'
    per_page = settings.LIST_PER_PAGE_INLINE

    option_no.short_description = _('option no')
    option_key.short_description = _('option id')

    product_id = None

    def get_formset(self, request, obj=None, **kwargs):
        self.product_id = obj.product_id
        formset_class = super(LicenseOptionTabular, self).get_formset(
            request, obj, **kwargs)

        form = formset_class.form
        # hidden add/change FK
        try:

            if self.has_change_permission(request):
                form.base_fields['option'].widget.can_change_related = False
            if self.has_add_permission(request):
                form.base_fields['option'].widget.can_add_related = False
        except (KeyError, TypeError) as e:
            print('Error get_formset LicenseOptionTabular: %s' % e)
            messages.error(request, _(
                'An unexpected error has occurred. Please contact your system administrator. ') + 'Error get_formset LicenseOptionTabular: %s' % e)

        class PaginationFormSet(formset_class):
            def __init__(self, *args, **kwargs):
                super(PaginationFormSet, self).__init__(*args, **kwargs)

                qs = self.queryset
                paginator = Paginator(qs, self.per_page)
                try:
                    page_num = int(request.GET.get('p', '0'))
                except ValueError:
                    page_num = 0

                try:
                    page = paginator.page(page_num + 1)
                except (EmptyPage, InvalidPage):
                    page = paginator.page(paginator.num_pages)

                self.cl = InlineChangeList(request, page_num, paginator)
                self.paginator = paginator

                if self.cl.show_all:
                    self._queryset = qs
                else:
                    self._queryset = page.object_list

        PaginationFormSet.per_page = self.per_page
        return PaginationFormSet

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "option":
            return OptionChoiceField(queryset=Option.objects.all().filter(product=self.product_id))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class LicenseAdmin(AdminAdvancedFiltersMixin, admin.ModelAdmin):
    change_form_template = 'admin/custom/change_form_key.html'
    inlines = (LicenseOptionTabular, ActivationInline)
    list_display = ('license_key', 'get_user', 'get_user_profile_full_name_kanji', 'license_expiration', 'get_product',
                    'get_list_option', 'activate_expiration', 'activation_pass', 'start_app_num', 'pause')
    list_display_links = ('get_user', 'license_key', 'get_product')
    advanced_filter_fields = (
        'license_key',
        ('user__username', _('user')),
        ('user__profile__full_name_kanji', _('full name')),
        'license_expiration',
        ('product__product_name', _('product')),
        ('option__option_name', _('OP')),
        'activate_expiration',
        'activation_pass',
        'start_app_num',
        'pause',
        'created_date',
        'updated_date',
    )
    fields = (
        'license_key', 'user', 'custom_user', 'product', 'license_expiration', 'activate_expiration', 'activation_pass',
        'start_app_num', 'pause', 'created_date', 'updated_date'
    )
    # per_page pagination
    list_per_page = settings.LIST_PER_PAGE

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['product', 'custom_user', 'created_date', 'updated_date']
        else:
            return ['custom_user', 'created_date', 'updated_date']

    def custom_user(self, obj):
        return obj.user.profile.full_name_kanji

    custom_user.short_description = _('user')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'user':
            return UserFullnameChoiceField(queryset=User.objects.all())
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_user_profile_full_name_kanji(self, obj):
        return obj.user.profile.full_name_kanji

    def get_user(self, obj):
        return mark_safe("""<a href='/admin/user/user/%s/change'>%s</a>""" % (obj.user.id, obj.user.username))

    def get_product(self, obj):
        return mark_safe(
            """<a href='/admin/catalogue/product/%s/change'>%s</a>""" % (obj.product.id, obj.product.product_name))

    def get_list_option(self, obj):
        return ', '.join([o.option_name + ' (' + o.option_no + ')' for o in
                          obj.option.all().order_by('licenseoption__purchase_date')])

    def get_form(self, request, obj=None, **kwargs):
        form = super(LicenseAdmin, self).get_form(request, obj, **kwargs)
        try:
            if self.has_change_permission(request):
                form.base_fields['user'].widget.can_change_related = False
            if self.has_add_permission(request):
                form.base_fields['user'].widget.can_add_related = False
        except (KeyError, TypeError) as e:
            print('Error get_form LicenseAdmin: %s' % e)
            messages.error(request, _(
                'An unexpected error has occurred. Please contact your system administrator. ') + 'Error get_form LicenseAdmin: %s' % e)
        return form

    # title
    get_user_profile_full_name_kanji.short_description = _('full name')
    get_user.short_description = _('user')
    get_product.short_description = _('product')
    get_list_option.short_description = _('OP')

    # sort
    get_user_profile_full_name_kanji.admin_order_field = 'user__profile__full_name_kanji'
    get_user.admin_order_field = 'user__username'
    get_product.admin_order_field = 'product'

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(LicenseAdmin, self).get_inline_instances(request, obj)


admin.site.register(License, LicenseAdmin)
