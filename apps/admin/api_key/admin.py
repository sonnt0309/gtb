from django.contrib import admin
from .models import ApiKey
from django.utils.translation import ugettext_lazy as _
from django.conf import settings


# Register your models here.
class ApiKeyAdmin(admin.ModelAdmin):
    change_list_template = 'admin/custom/template_api_key.html'


admin.site.register(ApiKey, ApiKeyAdmin)
