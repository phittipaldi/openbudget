# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-22 20:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0013_periodtype_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='periodtype',
            name='code',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
    ]
