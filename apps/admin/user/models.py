from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser, UserManager
from django.db.models.query import QuerySet
from django.db.models.signals import post_save
from django.utils import timezone
from django.dispatch import receiver
from helper import validate


class UserAccountManager(UserManager):
    def __init__(self, *args, **kwargs):
        self.alive_only = kwargs.pop('alive_only', True)
        super(UserAccountManager, self).__init__(*args, **kwargs)

    def get_queryset(self):
        if self.alive_only:
            return SoftDeletionQuerySet(self.model).filter(is_deleted=False)
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


# Create your models here.
class User(AbstractUser):
    is_deleted = models.BooleanField(default=False, verbose_name=_('is deleted'))

    objects = UserAccountManager()
    all_objects = UserAccountManager(alive_only=False)

    class Meta:
        db_table = 'auth_user'
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def delete(self):
        self.is_deleted = True
        self.save()

    def hard_delete(self):
        super(User, self).delete()


# locale: 1: English, 2: Japanese, 3:Chinese
class Profile(models.Model):
    LOCALE_CHOICES = (
        ('EN', _('English')),
        ('JA', _('Japanese')),
        ('ZH-HANS', _('Chinese')),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    activation_pass = models.CharField(max_length=150, verbose_name=_('activation pass'), validators=[validate.validate_activation_pass])
    first_name_furi = models.CharField(max_length=30, blank=True, verbose_name=_('first name furigana'), validators=[validate.validate_furi])
    last_name_furi = models.CharField(max_length=150, blank=True, verbose_name=_('last name furigana'), validators=[validate.validate_furi])
    department_kanji = models.CharField(max_length=150, blank=True, verbose_name=_('department'))
    department_furi = models.CharField(max_length=150, blank=True, verbose_name=_('department furigana'), validators=[validate.validate_furi])
    address_kanji = models.CharField(max_length=150, verbose_name=_('address'))
    address_furi = models.CharField(max_length=150, blank=True, verbose_name=_('address furigana'), validators=[validate.validate_address_furi])
    tel = models.CharField(max_length=13, verbose_name=_('tel'), validators=[validate.validate_tel])
    postal_code = models.CharField(max_length=8, verbose_name=_('postal code'), validators=[validate.validate_postal_code])
    created_date = models.DateTimeField(default=timezone.now, verbose_name=_('created date'))
    updated_date = models.DateTimeField(default=timezone.now, verbose_name=_('updated date'))
    locale = models.CharField(max_length=10, verbose_name=_('locale'), choices=LOCALE_CHOICES)
    first_name_kanji = models.CharField(max_length=30, verbose_name=_('first name'))
    last_name_kanji = models.CharField(max_length=150, verbose_name=_('last name'))
    company = models.CharField(max_length=150, verbose_name=_('company'))
    company_furi = models.CharField(max_length=150, blank=True, verbose_name=_('company furigana'), validators=[validate.validate_furi])
    full_name_kanji = models.CharField(max_length=200, blank=True, verbose_name=_('full name'))
    full_name_furi = models.CharField(max_length=200, blank=True, null=True, verbose_name=_('full name furi'))

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        full_name_kanji = "%s %s" % (self.last_name_kanji, self.first_name_kanji)
        full_name_furi = "%s %s" % (self.last_name_furi, self.first_name_furi)
        self.full_name_kanji = full_name_kanji.strip()
        self.full_name_furi = full_name_furi.strip()
        self.updated_date = timezone.now()
        super(Profile, self).save(*args, **kwargs)


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
