from django.db import models
from django.db.models.query import QuerySet
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator, MinLengthValidator
from django.utils.crypto import get_random_string
from helper.validate import validate_key
from apps.custom_oscar.catalogue.models import Product


# Create your models here.
class SoftDeletionManager(models.Manager):
    def __init__(self, *args, **kwargs):
        self.alive_only = kwargs.pop('alive_only', True)
        super(SoftDeletionManager, self).__init__(*args, **kwargs)

    def get_queryset(self):
        if self.alive_only:
            # Show record deleted
            # return SoftDeletionQuerySet(self.model).filter(deleted_at__isnull=False)

            # Show record not deleted
            return SoftDeletionQuerySet(self.model).filter(product__is_deleted=False).filter(is_deleted=False)

            # Show record all
            # return SoftDeletionQuerySet(self.model)
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


class Option(models.Model):
    option_key = models.CharField(max_length=6, unique=True, validators=[MinLengthValidator(6), validate_key], verbose_name=_('option id'))
    option_no = models.CharField(max_length=50, verbose_name=_('option no'))
    option_name = models.CharField(max_length=250, verbose_name=_('option name'))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_('product'))
    is_deleted = models.BooleanField(default=False, verbose_name=_('is deleted'))
    created_date = models.DateTimeField(default=timezone.now, verbose_name=_('created date'))
    updated_date = models.DateTimeField(default=timezone.now, verbose_name=_('updated date'))

    objects = SoftDeletionManager()
    all_objects = SoftDeletionManager(alive_only=False)

    class Meta:
        verbose_name = _('option')
        verbose_name_plural = _('options')

    def __str__(self):
        return self.option_name

    def save(self, *args, **kwargs):
        if not self.pk and not self.option_key:
            self.option_key = get_random_string(length=6)
        self.updated_date = timezone.now()
        super(Option, self).save(*args, **kwargs)

    def delete(self):
        self.is_deleted = True
        self.save()

    def hard_delete(self):
        super(Option, self).delete()
