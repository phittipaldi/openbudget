# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-04-06 21:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0053_templatefile_split_char'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='formatdate',
            name='value',
        ),
        migrations.AddField(
            model_name='formatdate',
            name='has_year',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='formatdate',
            name='pos_day',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='formatdate',
            name='pos_month',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='formatdate',
            name='pos_year',
            field=models.IntegerField(default=0),
        ),
    ]
