# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-04-06 17:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0050_auto_20180405_1513'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bank',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=b'banks'),
        ),
        migrations.AlterField(
            model_name='bank',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]