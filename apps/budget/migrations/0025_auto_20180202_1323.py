# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-02-02 13:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0024_auto_20180202_1029'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subcategory',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subcategories', to='budget.Category'),
        ),
    ]
