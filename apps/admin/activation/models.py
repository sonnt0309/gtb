from django.db import models
from django.utils import timezone
from apps.admin.license.models import License
from django.db.models.query import QuerySet
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator, MinLengthValidator
from django.utils.crypto import get_random_string
from helper import validate
from django.core.exceptions import ValidationError


# Create your models here.
class SoftDeletionManager(models.Manager):
    def __init__(self, *args, **kwargs):
        self.alive_only = kwargs.pop('alive_only', True)
        super(SoftDeletionManager, self).__init__(*args, **kwargs)

    def get_queryset(self):
        if self.alive_only:
            return SoftDeletionQuerySet(self.model).filter(license__product__is_deleted=False).filter(license__user__is_deleted=False).filter(license__is_deleted=False).filter(is_deleted=False)
        return SoftDeletionQuerySet(self.model)

    def hard_delete(self):
        return self.get_queryset().hard_delete()


class SoftDeletionQuerySet(QuerySet):
    def delete(self):
        return super(SoftDeletionQuerySet, self).update(is_deleted=True)

    def hard_delete(self):
        return super(SoftDeletionQuerySet, self).delete()

    def alive(self):
        return self.filter(is_deleted=False)

    def dead(self):
        return self.exclude(is_deleted=False)


class Activation(models.Model):
    activate_key = models.CharField(max_length=6, null=False, verbose_name=_('Activate ID'), unique=True, validators=[MinLengthValidator(6), validate.validate_key])
    license = models.ForeignKey(License, on_delete=models.CASCADE, verbose_name=_('license'))
    activate_date_time = models.DateTimeField(default=timezone.now, verbose_name=_('activate date'))
    pc_name = models.CharField(max_length=150, null=False, verbose_name=_('pc name'))
    windows_product_id = models.CharField(max_length=29, null=False, verbose_name=_('windows product ID'))
    mac_address = models.CharField(max_length=20, null=False, verbose_name=_('mac address'))
    drive_serial_number = models.CharField(max_length=20, null=False, verbose_name=_('drive serial number'))
    activate_status_code = models.CharField(max_length=5, verbose_name=_('activate status code'), validators=[validate.validate_activate_status_code])
    is_deleted = models.BooleanField(default=False, verbose_name=_('is deleted'))
    created_date = models.DateTimeField(default=timezone.now, verbose_name=_('created date'))
    updated_date = models.DateTimeField(default=timezone.now, verbose_name=_('updated date'))

    objects = SoftDeletionManager()
    all_objects = SoftDeletionManager(alive_only=False)

    class Meta:
        verbose_name = _('activation')
        verbose_name_plural = _('activations')

    def __str__(self):
        return self.activate_key

    def save(self, *args, **kwargs):
        if not self.pk and not self.activate_key:
            self.activate_key = get_random_string(length=6)
        self.updated_date = timezone.now()
        super(Activation, self).save(*args, **kwargs)

    def delete(self):
        self.is_deleted = True
        self.save()

    def hard_delete(self):
        super(Activation, self).delete()
