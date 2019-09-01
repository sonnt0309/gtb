from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class LicenseConfig(AppConfig):
    name = 'apps.admin.license'
    verbose_name = _("License")
