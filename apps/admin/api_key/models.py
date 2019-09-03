from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone


# Create your models here.
class ApiKey(models.Model):
    public_key = models.TextField(null=False, verbose_name=_('public key'))
    created_date = models.DateTimeField(default=timezone.now, verbose_name=_('created date'))
    updated_date = models.DateTimeField(default=timezone.now, verbose_name=_('updated date'))

    class Meta:
        verbose_name = _('Key')
        verbose_name_plural = _('Keys')

    def __unicode__(self):
        return self.public_key