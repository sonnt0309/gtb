from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from apps.admin.activation.models import Activation
from django.db.models.query import QuerySet
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator, MinLengthValidator
from django.utils.crypto import get_random_string
from django.core.exceptions import ValidationError
from helper.validate import isInteger, validate_key


def validate_status_code(value):
    for characters in value:
        if not isInteger(characters):
            raise ValidationError(
                _('Is not number'),
            )


# Create your models here.
class SoftDeletionManager(models.Manager):
    def __init__(self, *args, **kwargs):
        self.alive_only = kwargs.pop('alive_only', True)
        super(SoftDeletionManager, self).__init__(*args, **kwargs)

    def get_queryset(self):
        if self.alive_only:
            return SoftDeletionQuerySet(self.model).filter(activation__license__user__is_deleted=False).filter(
                activation__license__product__is_deleted=False).filter(activation__license__is_deleted=False).filter(
                activation__is_deleted=False).filter(is_deleted=False)
        return SoftDeletionQuerySet(self.model)

    def hard_delete(self):
        return self.get_queryset().hard_delete()

    def create_status(self, activation, app_exe_status_key, status_code, exe_status_expiration):
        rs = self.create(
            activation=activation,
            app_exe_status_key=app_exe_status_key,
            status_code=status_code,
            exe_status_expiration=exe_status_expiration)
        # do something with the book
        return rs


class SoftDeletionQuerySet(QuerySet):
    def delete(self):
        return super(SoftDeletionQuerySet, self).update(is_deleted=True)

    def hard_delete(self):
        return super(SoftDeletionQuerySet, self).delete()

    def alive(self):
        return self.filter(is_deleted=False)

    def dead(self):
        return self.exclude(is_deleted=False)


class ExecutionStatus(models.Model):
    activation = models.ForeignKey(Activation, on_delete=models.CASCADE, verbose_name=_('activation'))
    app_exe_status_key = models.CharField(max_length=6, null=False, unique=True,
                                          validators=[MinLengthValidator(6), validate_key],
                                          verbose_name=_('app exe status ID'))
    start_app_datetime = models.DateTimeField(default=timezone.now, verbose_name=_('start app datetime'))
    status_last_update = models.DateTimeField(default=timezone.now, verbose_name=_('status last update'))
    status_code = models.CharField(max_length=5, verbose_name=_('status code'))
    exe_status_expiration = models.DateTimeField(default=timezone.now, verbose_name=_('exe status expiration'))
    is_deleted = models.BooleanField(default=False, verbose_name=_('is deleted'))
    created_date = models.DateTimeField(default=timezone.now, verbose_name=_('created date'))
    updated_date = models.DateTimeField(default=timezone.now, verbose_name=_('updated date'))

    objects = SoftDeletionManager()
    all_objects = SoftDeletionManager(alive_only=False)

    class Meta:
        verbose_name = _('execution status')
        verbose_name_plural = _('execution status')

    def __str__(self):
        return self.app_exe_status_key

    def save(self, *args, **kwargs):
        if not self.pk and not self.app_exe_status_key:
            self.app_exe_status_key = get_random_string(length=6)
        self.updated_date = timezone.now()
        self.status_last_update = timezone.now()
        super(ExecutionStatus, self).save(*args, **kwargs)

    def delete(self):
        self.is_deleted = True
        self.save()

    def hard_delete(self):
        super(ExecutionStatus, self).delete()
