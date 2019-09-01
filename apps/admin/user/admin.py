from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile
from advanced_filters.admin import AdminAdvancedFiltersMixin
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.http import HttpResponseRedirect
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import (UserCreationForm, UserChangeForm)
from helper import validate
from helper.CategoryChoiceField import ProductChoiceField
from apps.admin.license.models import License
from apps.custom_oscar.catalogue.models import Product
from django.utils.safestring import mark_safe
from django.contrib.admin.views.main import ChangeList
from django.core.paginator import EmptyPage, InvalidPage, Paginator
from django.contrib.admin.views.main import ChangeList
from django.contrib import messages


# validate edit user
class MyUserChangeForm(UserChangeForm):
    # validator unique email
    def clean_email(self):
        email = self.cleaned_data['email']
        if isinstance(email, str) and email.strip() == '':
            raise ValidationError(
                _("This field is required."),
            )
        elif User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise ValidationError(
                _('This email already used'),
            )
        else:
            return email

    # validator characters english or number username
    def clean_username(self):
        username = self.cleaned_data['username']
        for character in username:
            if not (validate.isAlphaLowerCase(character) or validate.isAlphaUpperCase(character) or validate.isInteger(character) or character in validate.isAsciiSymbol()):
                raise ValidationError(_('Is not character english, number or @/./+/-/_'),)
        return username


# validate create user
class MyUserCreationForm(UserCreationForm):
    # validator characters english or number username
    def clean_username(self):
        username = self.cleaned_data['username']
        for character in username:
            if not (validate.isAlphaLowerCase(character) or validate.isAlphaUpperCase(character) or validate.isInteger(character) or character in validate.isAsciiSymbol()):
                raise ValidationError(_('Is not character english, number or @/./+/-/_'),)
        return username


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name = _('Profile')
    verbose_name_plural = _('Profile')

    fields = (
        ('last_name_kanji', 'first_name_kanji'),
        ('last_name_furi', 'first_name_furi'),
        'activation_pass',
        ('company', 'company_furi'),
        ('department_kanji', 'department_furi'),
        'postal_code',
        'address_kanji',
        'address_furi',
        'tel',
        'locale',
        'created_date', 'updated_date',
    )

    fk_name = 'user'
    readonly_fields = ('created_date', 'updated_date')


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


class LicenseInline(admin.TabularInline):
    model = License
    fields = (
        'get_license', 'license_expiration', 'product', 'get_product_key', 'get_list_option', 'activate_expiration',
        'activation_pass', 'start_app_num', 'pause',)
    readonly_fields = ('get_license', 'get_product_key', 'get_list_option')
    verbose_name_plural = _('License')
    extra = 0

    def get_license(self, obj):
        return mark_safe("""<a href='/admin/license/license/%s/change'>%s</a>""" % (obj.id, obj.license_key))

    def get_product_key(self, obj):
        return mark_safe("""<a href='/admin/catalogue/product/%s/change'>%s</a>""" % (obj.product.id, obj.product.product_key))

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'product':
            return ProductChoiceField(queryset=Product.objects.all())
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        qs = super(LicenseInline, self).get_queryset(request)
        return qs.order_by('created_date')

    def get_list_option(self, obj):
        return ', '.join([o.option_name + ' (' + o.option_no + ')' for o in
                          obj.option.all().order_by('licenseoption__purchase_date')])

    get_license.short_description = _('license')
    get_product_key.short_description = _('product ID')
    get_list_option.short_description = _('OP')

    template = 'admin/edit_inline/tabular_paginated.html'
    per_page = 10

    def get_formset(self, request, obj=None, **kwargs):
        formset_class = super(LicenseInline, self).get_formset(
            request, obj, **kwargs)
        try:
            form = formset_class.form
            # hidden add/change FK
            if self.has_change_permission(request):
                form.base_fields['product'].widget.can_change_related = False
            if self.has_add_permission(request):
                form.base_fields['product'].widget.can_add_related = False
        except (KeyError, TypeError) as e:
            print('Error get_formset LicenseInline: %s' % e)
            messages.error(request, _('An unexpected error has occurred. Please contact your system administrator. ') + 'Error get_formset LicenseInline: %s' % e)

        # pagination
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


class UserAdmin(AdminAdvancedFiltersMixin, UserAdmin):
    inlines = (
        ProfileInline,
        LicenseInline,
    )
    form = MyUserChangeForm
    add_form = MyUserCreationForm
    list_display = (
        'username',
        'get_profile_last_name_kanji',
        'get_profile_first_name_kanji',
        'get_profile_activation_pass',
        'get_profile_compamy',
        'get_profile_company_furi',
        'get_profile_department_kanji',
        'get_profile_address_kanji',
        'get_profile_address_furi',
        'get_profile_telephone',
        'email',
        'is_active',
        'last_login',
    )
    advanced_filter_fields = (
        'username',
        ('profile__last_name_kanji', _('last name')),
        ('profile__first_name_kanji', _('first name')),
        ('profile__activation_pass', _('activation pass')),
        ('profile__company', _('company')),
        ('profile__company_furi', _('company furigana')),
        ('profile__department_kanji', _('department')),
        ('profile__address_kanji', _('address')),
        ('profile__address_furi', _('address furigana')),
        ('profile__tel', _('tel')),
        'email',
        'is_active',
        'last_login',
        ('profile__created_date', _('created date')),
        ('profile__updated_date', _('updated date')),
    )

    fieldsets = (
        (None, {'fields': ('username', 'password', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    def get_profile_full_name_kanji(self, obj):
        return obj.profile.full_name_kanji

    def get_profile_activation_pass(self, obj):
        return obj.profile.activation_pass

    def get_profile_first_name_kanji(self, obj):
        return obj.profile.first_name_kanji

    def get_profile_last_name_kanji(self, obj):
        return obj.profile.last_name_kanji

    def get_profile_department_kanji(self, obj):
        return obj.profile.department_kanji

    def get_profile_address_kanji(self, obj):
        return obj.profile.address_kanji

    def get_profile_address_furi(self, obj):
        return obj.profile.address_furi

    def get_profile_telephone(self, obj):
        return obj.profile.tel

    def get_profile_compamy(self, obj):
        return obj.profile.company

    def get_profile_company_furi(self, obj):
        return obj.profile.company_furi

    # title field
    get_profile_full_name_kanji.short_description = _('full name')
    get_profile_first_name_kanji.short_description = _('first name')
    get_profile_last_name_kanji.short_description = _('last name')
    get_profile_activation_pass.short_description = _('activation pass')
    get_profile_department_kanji.short_description = _('department')
    get_profile_address_kanji.short_description = _('address')
    get_profile_address_furi.short_description = _('address furigana')
    get_profile_telephone.short_description = _('tel')
    get_profile_compamy.short_description = _('company')
    get_profile_company_furi.short_description = _('company furigana')

    # sort field
    get_profile_full_name_kanji.admin_order_field = 'profile__full_name_kanji'
    get_profile_first_name_kanji.admin_order_field = 'profile__first_name_kanji'
    get_profile_last_name_kanji.admin_order_field = 'profile__last_name_kanji'
    get_profile_activation_pass.admin_order_field = 'profile__activation_pass'
    get_profile_department_kanji.admin_order_field = 'profile__department_kanji'
    get_profile_address_kanji.admin_order_field = 'profile__address_kanji'
    get_profile_address_furi.admin_order_field = 'profile__address_furi'
    get_profile_telephone.admin_order_field = 'profile__tel'
    get_profile_compamy.admin_order_field = 'profile__company'
    get_profile_company_furi.admin_order_field = 'profile__company_furi'

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(UserAdmin, self).get_inline_instances(request, obj)


admin.site.register(User, UserAdmin)
