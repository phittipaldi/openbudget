# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-02 10:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0005_auto_20171231_1109'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='date',
            field=models.DateTimeField(),
        ),
    ]
