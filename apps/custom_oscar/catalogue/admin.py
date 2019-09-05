from oscar.apps.catalogue.admin import *
from django.contrib import admin
from .models import Product
from django.contrib import messages
from helper.CategoryChoiceField import UserFullnameChoiceField
from django.utils.translation import ugettext_lazy as _
from django.core.paginator import EmptyPage, InvalidPage, Paginator
from django.utils.safestring import mark_safe
from django.contrib.admin.views.main import ChangeList
from apps.admin.license.models import License
from apps.admin.option.models import Option
from apps.admin.user.models import User
from django.conf import settings


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
    fields = ('get_license', 'license_expiration', 'user', 'get_options', 'activate_expiration', 'activation_pass', 'start_app_num', 'pause',)
    readonly_fields = ('get_license', 'get_options')
    verbose_name_plural = _('License')
    extra = 0

    def get_license(self, obj):
        return mark_safe("""<a href='/admin/license/license/%s/change'>%s</a>""" % (obj.id, obj.license_key))

    def get_options(self, obj):
        return ', '.join([o.option_name + ' (' + o.option_no + ')' for o in
                          obj.option.all().order_by('licenseoption__purchase_date')])

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'user':
            return UserFullnameChoiceField(queryset=User.objects.all())
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    get_license.short_description = _('license')
    get_options.short_description = _('OP')

    template = 'admin/edit_inline/tabular_paginated.html'
    per_page = settings.LIST_PER_PAGE_INLINE

    def get_formset(self, request, obj=None, **kwargs):
        formset_class = super(LicenseInline, self).get_formset(
            request, obj, **kwargs)
        try:
            form = formset_class.form
            # hidden add/change FK
            if self.has_change_permission(request):
                form.base_fields['user'].widget.can_change_related = False
            if self.has_add_permission(request):
                form.base_fields['user'].widget.can_add_related = False
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


class OptionInline(admin.TabularInline):
    model = Option
    fields = ('get_option', 'product', 'option_no', 'option_name',)
    readonly_fields = ('get_option',)
    verbose_name_plural = _('Option')
    extra = 0

    def get_option(self, obj):
        return mark_safe("""<a href='/admin/option/option/%s/change'>%s</a>""" % (obj.id, obj.option_key))

    get_option.short_description = _('option')

    template = 'admin/edit_inline/tabular_paginated.html'
    per_page = settings.LIST_PER_PAGE_INLINE

    def get_formset(self, request, obj=None, **kwargs):
        formset_class = super(OptionInline, self).get_formset(
            request, obj, **kwargs)
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


class ProductAdmin(admin.ModelAdmin):
    change_form_template = 'admin/custom/change_form_key.html'
    date_hierarchy = 'date_created'
    list_display = ('get_title', 'upc', 'get_product_class', 'structure',
                    'attribute_summary', 'date_created')
    list_filter = ['structure', 'is_discountable']
    raw_id_fields = ['parent']
    # inlines = [AttributeInline, CategoryInline, ProductRecommendationInline]
    inlines = [OptionInline, LicenseInline]
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ['upc', 'title']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return (
            qs
                .select_related('product_class', 'parent')
                .prefetch_related(
                'attribute_values',
                'attribute_values__attribute'))

    exclude = ('is_deleted',)


admin.site.unregister(Product)
admin.site.register(Product, ProductAdmin)
