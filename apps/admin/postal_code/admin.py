from django.contrib import admin
from .models import PostalCode
from django.utils.translation import ugettext_lazy as _
from advanced_filters.admin import AdminAdvancedFiltersMixin
from django.conf import settings


# Register your models here.
class PostalCodeAdmin(AdminAdvancedFiltersMixin, admin.ModelAdmin):
    search_fields = ('zip',)
    list_display = (
        'zip', 'ken_id', 'city_id', 'town_id', 'office_flg', 'delete_flg', 'ken_name', 'ken_furi', 'city_name',
        'city_furi', 'town_name', 'town_furi', 'town_memo', 'kyoto_street', 'block_name', 'block_furi', 'memo',
        'office_furi', 'office_address', 'new_id'
    )
    advanced_filter_fields = (
        'zip', 'ken_id', 'city_id', 'town_id', 'office_flg', 'delete_flg', 'ken_name', 'ken_furi', 'city_name',
        'city_furi', 'town_name', 'town_furi', 'town_memo', 'kyoto_street', 'block_name', 'block_furi', 'memo',
        'office_furi', 'office_address', 'new_id'
    )
    # hidden fields
    exclude = ('is_deleted', 'created_date', 'updated_date')
    # per_page pagination
    list_per_page = settings.LIST_PER_PAGE


admin.site.register(PostalCode, PostalCodeAdmin)
