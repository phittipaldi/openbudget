# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-03-18 12:41
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0036_auto_20180318_1231'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recurrentshedule',
            name='user_insert',
        ),
        migrations.RemoveField(
            model_name='recurrentshedule',
            name='user_update',
        ),
    ]