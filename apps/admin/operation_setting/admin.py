from django.contrib import admin
from advanced_filters.admin import AdminAdvancedFiltersMixin
from .models import OperationSetting
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from helper.CategoryChoiceField import ProductChoiceField
from django.utils.safestring import mark_safe
from apps.custom_oscar.catalogue.models import Product
from django.contrib import messages


# Register your models here.
class OperationSettingAdmin(AdminAdvancedFiltersMixin, admin.ModelAdmin):
    change_form_template = 'admin/custom/change_form_key.html'
    list_display = ('operation_setting_key', 'get_product', 'check_interval_seconds', 'status_valid_seconds', 'latest_version', 'oldest_version',)
    advanced_filter_fields = (
        'operation_setting_key',
        'product__product_key',
        'check_interval_seconds',
        'status_valid_seconds',
        'latest_version',
        'oldest_version',
        'created_date',
        'updated_date',
    )
    fields = (
        'operation_setting_key',
        'product',
        'check_interval_seconds',
        'status_valid_seconds',
        'latest_version',
        'oldest_version',
        'created_date',
        'updated_date',
    )
    readonly_fields = ('created_date', 'updated_date',)
    # hidden fields
    exclude = ('is_deleted',)
    # per_page pagination
    list_per_page = settings.LIST_PER_PAGE

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'product':
            return ProductChoiceField(queryset=Product.objects.all())
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_product(self, obj):
        return mark_safe("""<a href='/admin/catalogue/product/%s/change'>%s</a>""" % (obj.product.id, obj.product.product_name))

    def get_form(self, request, obj=None, **kwargs):
        form = super(OperationSettingAdmin, self).get_form(request, obj, **kwargs)
        try:
            if self.has_change_permission(request):
                form.base_fields['product'].widget.can_change_related = False
            if self.has_add_permission(request):
                form.base_fields['product'].widget.can_add_related = False
        except (KeyError, TypeError) as e:
            print('Error get_form OperationSettingCustom: %s' % e)
            messages.error(request, _('An unexpected error has occurred. Please contact your system administrator. ') + 'Error get_form OperationSettingAdmin: %s' % e)
        return form

    get_product.short_description = _('product')
    get_product.admin_order_field = 'product'


admin.site.register(OperationSetting, OperationSettingAdmin)
