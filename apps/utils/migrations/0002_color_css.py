# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-04 09:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='color',
            name='css',
            field=models.CharField(default=1, max_length=30),
            preserve_default=False,
        ),
    ]