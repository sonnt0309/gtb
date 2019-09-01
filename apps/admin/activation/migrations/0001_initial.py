# Generated by Django 2.2.3 on 2019-09-01 06:43

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import helper.validate


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('license', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activate_key', models.CharField(max_length=6, unique=True, validators=[django.core.validators.MinLengthValidator(6), helper.validate.validate_key], verbose_name='Activate ID')),
                ('activate_date_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='activate date')),
                ('pc_name', models.CharField(max_length=150, verbose_name='pc name')),
                ('windows_product_id', models.CharField(max_length=29, verbose_name='windows product ID')),
                ('mac_address', models.CharField(max_length=20, verbose_name='mac address')),
                ('drive_serial_number', models.CharField(max_length=20, verbose_name='drive serial number')),
                ('activate_status_code', models.CharField(max_length=5, validators=[helper.validate.validate_activate_status_code], verbose_name='activate status code')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='is deleted')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='created date')),
                ('updated_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='updated date')),
                ('license', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='license.License', verbose_name='license')),
            ],
            options={
                'verbose_name': 'activation',
                'verbose_name_plural': 'activations',
            },
        ),
    ]