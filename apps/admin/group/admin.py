from django.contrib import admin
from advanced_filters.admin import AdminAdvancedFiltersMixin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import GroupAdmin
# Register your models here.


class SearchGroup(AdminAdvancedFiltersMixin, GroupAdmin):
    list_display = ('name',)
    advanced_filter_fields = (
        'name',
    )


admin.site.unregister(Group)
admin.site.register(Group, SearchGroup)