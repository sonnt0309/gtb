from django.db import models
from django.db.models.query import QuerySet
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator, MinLengthValidator
from django.utils.crypto import get_random_string
from apps.admin.user.models import User
from apps.admin.option.models import Option
from apps.custom_oscar.catalogue.models import Product
from django.utils import timezone
from helper import validate


# Create your models here.
class SoftDeletionManager(models.Manager):
    def __init__(self, *args, **kwargs):
        self.alive_only = kwargs.pop('alive_only', True)
        super(SoftDeletionManager, self).__init__(*args, **kwargs)

    def get_queryset(self):
        if self.alive_only:
            return SoftDeletionQuerySet(self.model).filter(product__is_deleted=False).filter(user__is_deleted=False).filter(is_deleted=False)
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


class License(models.Model):
    license_key = models.CharField(max_length=6, verbose_name=_('License ID'), unique=True, validators=[MinLengthValidator(6), validate.validate_key])
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('user'))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_('product'))
    license_expiration = models.DateTimeField(verbose_name=_('expiration date'))
    activate_expiration = models.DateTimeField(verbose_name=_('activation date'))
    activation_pass = models.CharField(max_length=128, blank=True, verbose_name=_('activation pass'), validators=[validate.validate_activation_pass])
    is_deleted = models.BooleanField(default=False, verbose_name=_('is deleted'))
    created_date = models.DateTimeField(default=timezone.now, verbose_name=_('created date'))
    updated_date = models.DateTimeField(default=timezone.now, verbose_name=_('updated date'))
    option = models.ManyToManyField(Option, through='LicenseOption', verbose_name=_('option'))
    start_app_num = models.IntegerField(validators=[MinValueValidator(0, _('Only input number 0-9'))], verbose_name=_('app start number'))
    pause = models.BooleanField(verbose_name=_('pause'), default=False)

    objects = SoftDeletionManager()
    all_objects = SoftDeletionManager(alive_only=False)

    class Meta:
        verbose_name = _('license')
        verbose_name_plural = _('licenses')

    def __str__(self):
        return self.license_key

    def save(self, *args, **kwargs):
        if not self.pk and not self.license_key:
            self.license_key = get_random_string(length=6)
        self.updated_date = timezone.now()
        super(License, self).save(*args, **kwargs)

    def delete(self):
        self.is_deleted = True
        self.save()

    def hard_delete(self):
        super(License, self).delete()


class LicenseOption(models.Model):
    option = models.ForeignKey(Option, on_delete=models.CASCADE, verbose_name=_('option'))
    license = models.ForeignKey(License, on_delete=models.CASCADE, verbose_name=_('license'))
    purchase_date = models.DateTimeField(verbose_name=_('purchase date'))
    is_deleted = models.BooleanField(default=False, verbose_name=_('is deleted'))
    created_date = models.DateTimeField(default=timezone.now, verbose_name=_('created date'))
    updated_date = models.DateTimeField(default=timezone.now, verbose_name=_('updated date'))

    def __str__(self):
        return self.option.option_key + self.license.license_key

    class Meta:
        verbose_name = _('license option')
        verbose_name_plural = _('license options')
