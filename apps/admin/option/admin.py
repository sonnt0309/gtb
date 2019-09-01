from django.contrib import admin
from .models import Option
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from advanced_filters.admin import AdminAdvancedFiltersMixin
from django.contrib import messages
from helper.CategoryChoiceField import ProductNameIDChoiceField
from apps.custom_oscar.catalogue.models import Product


# Register your models here.
class OptionAdmin(AdminAdvancedFiltersMixin, admin.ModelAdmin):
    change_form_template = 'admin/custom/change_form_key.html'
    list_display = ('option_key', 'product', 'option_no', 'option_name',)
    readonly_fields = ('created_date', 'updated_date')
    # hidden fields
    exclude = ('is_deleted',)
    # fields search
    advanced_filter_fields = (
        'option_key',
        'product',
        'option_no',
        'option_name',
        'created_date',
        'updated_date'
    )
    # per_page pagination
    list_per_page = settings.LIST_PER_PAGE

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "product":
            return ProductNameIDChoiceField(queryset=Product.objects.all())
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_form(self, request, obj=None, **kwargs):
        form = super(OptionAdmin, self).get_form(request, obj, **kwargs)
        try:
            if self.has_change_permission(request):
                form.base_fields['product'].widget.can_change_related = False
            if self.has_add_permission(request):
                form.base_fields['product'].widget.can_add_related = False
        except (KeyError, TypeError) as e:
            print('Error get_form OptionAdmin: %s' % e)
            messages.error(request, _('An unexpected error has occurred. Please contact your system administrator. ') + 'Error get_form OptionAdmin: %s' % e)
        return form


admin.site.register(Option, OptionAdmin)
