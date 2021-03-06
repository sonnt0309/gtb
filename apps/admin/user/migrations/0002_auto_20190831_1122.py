# Generated by Django 2.2.3 on 2019-08-31 04:22

import apps.admin.user.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import helper.validate


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', apps.admin.user.models.UserAccountManager()),
                ('all_objects', apps.admin.user.models.UserAccountManager(alive_only=False)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activation_pass', models.CharField(max_length=150, validators=[helper.validate.validate_activation_pass], verbose_name='activation pass')),
                ('first_name_furi', models.CharField(blank=True, max_length=30, validators=[helper.validate.validate_furi], verbose_name='first name furigana')),
                ('last_name_furi', models.CharField(blank=True, max_length=150, validators=[helper.validate.validate_furi], verbose_name='last name furigana')),
                ('department_kanji', models.CharField(blank=True, max_length=150, verbose_name='department')),
                ('department_furi', models.CharField(blank=True, max_length=150, validators=[helper.validate.validate_furi], verbose_name='department furigana')),
                ('address_kanji', models.CharField(max_length=150, verbose_name='address')),
                ('address_furi', models.CharField(blank=True, max_length=150, validators=[helper.validate.validate_address_furi], verbose_name='address furigana')),
                ('tel', models.CharField(max_length=13, validators=[helper.validate.validate_tel], verbose_name='tel')),
                ('postal_code', models.CharField(max_length=8, validators=[helper.validate.validate_postal_code], verbose_name='postal code')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='created date')),
                ('updated_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='updated date')),
                ('locale', models.CharField(choices=[('EN', 'English'), ('JA', 'Japanese'), ('ZH-HANS', 'Chinese')], max_length=10, verbose_name='locale')),
                ('first_name_kanji', models.CharField(max_length=30, verbose_name='first name')),
                ('last_name_kanji', models.CharField(max_length=150, verbose_name='last name')),
                ('company', models.CharField(max_length=150, verbose_name='company')),
                ('company_furi', models.CharField(blank=True, max_length=150, validators=[helper.validate.validate_furi], verbose_name='company furigana')),
                ('full_name_kanji', models.CharField(blank=True, max_length=200, verbose_name='full name')),
                ('full_name_furi', models.CharField(blank=True, max_length=200, null=True, verbose_name='full name furi')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
