# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-02-01 18:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0019_auto_20180130_1946'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='budgetperiod',
            name='period_type',
        ),
        migrations.AddField(
            model_name='budgetperiod',
            name='budget',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='budget.Budget'),
            preserve_default=False,
        ),
    ]