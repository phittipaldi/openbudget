# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-03-22 14:01
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0041_recurrentshedule_is_pending'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recurrentshedule',
            name='is_pending',
        ),
    ]
