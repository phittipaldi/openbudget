# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-03-22 14:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0044_auto_20180322_1430'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recurrentsheduleline',
            name='shedule',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lines', to='budget.RecurrentShedule'),
        ),
    ]