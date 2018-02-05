# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-27 10:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0015_auto_20180123_0911'),
    ]

    operations = [
        migrations.CreateModel(
            name='DurationFilter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('value', models.IntegerField()),
                ('is_day', models.BooleanField(default=True)),
                ('is_month', models.BooleanField(default=False)),
                ('is_year', models.BooleanField(default=False)),
            ],
        ),
    ]