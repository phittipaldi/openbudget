# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-04 09:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0006_auto_20180102_1025'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='place',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='photo',
            field=models.FileField(blank=True, null=True, upload_to=b'transactions'),
        ),
    ]
