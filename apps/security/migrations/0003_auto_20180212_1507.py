# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-02-12 15:07
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('security', '0002_activationpending'),
    ]

    operations = [
        migrations.RenameField(
            model_name='activationpending',
            old_name='experition_date',
            new_name='expiration_date',
        ),
    ]
