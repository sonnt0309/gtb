# Generated by Django 2.2.3 on 2019-08-31 06:37

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import helper.validate


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('catalogue', '0017_auto_20190831_1315'),
    ]

    operations = [
        migrations.CreateModel(
            name='Option',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('option_key', models.CharField(max_length=6, unique=True, validators=[django.core.validators.MinLengthValidator(6), helper.validate.validate_key], verbose_name='option id')),
                ('option_no', models.CharField(max_length=50, verbose_name='option no')),
                ('option_name', models.CharField(max_length=250, verbose_name='option name')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='is deleted')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='created date')),
                ('updated_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='updated date')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalogue.Product', verbose_name='product')),
            ],
            options={
                'verbose_name': 'option',
                'verbose_name_plural': 'options',
            },
        ),
    ]
