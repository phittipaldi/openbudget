# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-04-20 19:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0062_auto_20180411_1235'),
    ]

    operations = [
        migrations.AddField(
            model_name='transactionuploaded',
            name='trx_match',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='budget.Transaction'),
        ),
    ]
