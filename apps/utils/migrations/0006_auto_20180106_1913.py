# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-06 19:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0005_auto_20180106_1846'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='currency',
            name='owners',
        ),
        migrations.AlterField(
            model_name='currency',
            name='name',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.DeleteModel(
            name='CurrencyDescription',
        ),
    ]
