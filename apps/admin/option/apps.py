from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class OptionConfig(AppConfig):
    name = 'apps.admin.option'
    verbose_name = _("Option")
