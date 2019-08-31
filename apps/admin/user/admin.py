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


class UserAdmin(AdminAdvancedFiltersMixin, UserAdmin):
    inlines = (
        ProfileInline,
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
