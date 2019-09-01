from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ActivationConfig(AppConfig):
    name = 'apps.admin.activation'
    verbose_name = _("Activation")
