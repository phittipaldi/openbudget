# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-02-08 19:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0010_auto_20180208_0858'),
    ]

    operations = [
        migrations.AlterField(
            model_name='currencyrateline',
            name='value',
            field=models.DecimalField(decimal_places=4, max_digits=10),
        ),
    ]