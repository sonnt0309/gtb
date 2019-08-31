from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class PostalCodeConfig(AppConfig):
    name = 'apps.admin.postal_code'
    verbose_name = _("Postal code")
