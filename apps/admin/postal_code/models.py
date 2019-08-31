from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator, MinLengthValidator
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


# Create your models here.
class PostalCode(models.Model):
    ken_id = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(99)], verbose_name=_('ken id'), blank=True, null=True)
    city_id = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(99999)], verbose_name=_('city id'), blank=True, null=True)
    town_id = models.BigIntegerField(validators=[MinValueValidator(0), MaxValueValidator(999999999)], verbose_name=_('town id'), blank=True, null=True)
    zip = models.CharField(max_length=8, verbose_name=_('zip'), blank=True, null=True)
    office_flg = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(9)], verbose_name=_('office flg'), blank=True, null=True)
    delete_flg = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(9)], verbose_name=_('delete flg'), blank=True, null=True)
    ken_name = models.CharField(max_length=8, verbose_name=_('ken name'), blank=True, null=True)
    ken_furi = models.CharField(max_length=8, verbose_name=_('ken furi'), blank=True, null=True)
    city_name = models.CharField(max_length=24, verbose_name=_('city name'), blank=True, null=True)
    city_furi = models.CharField(max_length=24, verbose_name=_('city furi'), blank=True, null=True)
    town_name = models.CharField(max_length=32, verbose_name=_('town name'), blank=True, null=True)
    town_furi = models.CharField(max_length=32, verbose_name=_('town furi'), blank=True, null=True)
    town_memo = models.CharField(max_length=16, verbose_name=_('town memo'), blank=True, null=True)
    kyoto_street = models.CharField(max_length=32, verbose_name=_('kyoto street'), blank=True, null=True)
    block_name = models.CharField(max_length=64, verbose_name=_('block name'), blank=True, null=True)
    block_furi = models.CharField(max_length=64, verbose_name=_('block furi'), blank=True, null=True)
    memo = models.CharField(max_length=255, verbose_name=_('memo'), blank=True, null=True)
    office_name = models.CharField(max_length=255, verbose_name=_('office name'), blank=True, null=True)
    office_furi = models.CharField(max_length=255, verbose_name=_('office furi'), blank=True, null=True)
    office_address = models.CharField(max_length=255, verbose_name=_('office address'), blank=True, null=True)
    new_id = models.CharField(max_length=255, verbose_name=_('new id'), blank=True, null=True)
    is_deleted = models.BooleanField(default=False, verbose_name=_('is deleted'), blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now, verbose_name=_('created date'), blank=True, null=True)
    updated_date = models.DateTimeField(default=timezone.now, verbose_name=_('updated date'), blank=True, null=True)

    class Meta:
        verbose_name = _('postal code')
        verbose_name_plural = _('postal codes')

    def __str__(self):
        return self.zip
