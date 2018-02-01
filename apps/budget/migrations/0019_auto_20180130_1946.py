# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-30 19:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0018_auto_20180130_1800'),
    ]

    operations = [
        migrations.AlterField(
            model_name='budgetdetail',
            name='budget',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lines', to='budget.Budget'),
        ),
        migrations.AlterField(
            model_name='budgetline',
            name='budget',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='details', to='budget.Budget'),
        ),
    ]
