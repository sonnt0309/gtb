from django.db import models
from apps.custom_oscar.catalogue.models import Product
from django.utils import timezone
from django.db.models.query import QuerySet
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator, MinLengthValidator
from django.utils.crypto import get_random_string
from helper.validate import validate_key, validate_version


# Create your models here.
class SoftDeletionManager(models.Manager):
    def __init__(self, *args, **kwargs):
        self.alive_only = kwargs.pop('alive_only', True)
        super(SoftDeletionManager, self).__init__(*args, **kwargs)

    def get_queryset(self):
        if self.alive_only:
            return SoftDeletionQuerySet(self.model).filter(product__is_deleted=False).filter(is_deleted=False)
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


class OperationSetting(models.Model):
    operation_setting_key = models.CharField(max_length=6, verbose_name=_('operation setting ID'), unique=True, validators=[MinLengthValidator(6), validate_key])
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_('product'))
    check_interval_seconds = models.IntegerField(validators=[MinValueValidator(0)], verbose_name=_('check interval seconds'))
    status_valid_seconds = models.IntegerField(validators=[MinValueValidator(0)], verbose_name=_('status valid seconds'))
    latest_version = models.CharField(max_length=200, validators=[validate_version], verbose_name=_('latest version'))
    oldest_version = models.CharField(max_length=200, validators=[validate_version], verbose_name=_('oldest version'))
    is_deleted = models.BooleanField(default=False, verbose_name=_('is deleted'))
    created_date = models.DateTimeField(default=timezone.now, verbose_name=_('created date'))
    updated_date = models.DateTimeField(default=timezone.now, verbose_name=_('updated date'))

    objects = SoftDeletionManager()
    all_objects = SoftDeletionManager(alive_only=False)

    class Meta:
        verbose_name = _('operation setting')
        verbose_name_plural = _('operation setting')

    def __str__(self):
        return self.operation_setting_key

    def save(self, *args, **kwargs):
        if not self.pk and not self.operation_setting_key:
            self.operation_setting_key = get_random_string(length=6)
        self.updated_date = timezone.now()
        super(OperationSetting, self).save(*args, **kwargs)

    def delete(self):
        self.is_deleted = True
        self.save()

    def hard_delete(self):
        super(OperationSetting, self).delete()
