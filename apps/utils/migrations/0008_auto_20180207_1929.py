# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-02-07 19:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0007_currency_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='currency',
            name='code',
        ),
        migrations.AddField(
            model_name='currency',
            name='description',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
    ]
