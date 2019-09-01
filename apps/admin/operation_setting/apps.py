from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class OperationSettingConfig(AppConfig):
    name = 'apps.admin.operation_setting'
    verbose_name = _("Operation setting")
