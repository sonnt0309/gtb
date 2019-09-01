from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ExecutionStatusConfig(AppConfig):
    name = 'apps.admin.execution_status'
    verbose_name = _("Execution Status")
