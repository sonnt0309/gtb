from django.db import models
from oscar.apps.catalogue.abstract_models import AbstractProduct
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator, MinLengthValidator
from helper import validate
from django.utils.crypto import get_random_string
from django.utils import timezone


# Create your models here.
class Product(AbstractProduct):
    overview = models.TextField(verbose_name=_('Overview'), blank=True)
    product_key = models.CharField(max_length=6, unique=True, validators=[MinLengthValidator(6), validate.validate_key],
                                   verbose_name=_('product ID'))
    product_no = models.CharField(max_length=50, null=False, verbose_name=_('product no'))
    product_name = models.CharField(max_length=255, null=False, verbose_name=_('product name'))
    is_deleted = models.BooleanField(default=False, verbose_name=_('is deleted'))

    def save(self, *args, **kwargs):
        if not self.pk and not self.product_key:
            self.product_key = get_random_string(length=6)
        self.updated_date = timezone.now()
        super(Product, self).save(*args, **kwargs)


from oscar.apps.catalogue.models import *