# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-03-21 18:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0040_recurrentsheduleline'),
    ]

    operations = [
        migrations.AddField(
            model_name='recurrentshedule',
            name='is_pending',
            field=models.BooleanField(default=True),
        ),
    ]
