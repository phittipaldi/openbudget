# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-02-27 11:48
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('budget', '0030_auto_20180226_2001'),
    ]

    operations = [
        migrations.AddField(
            model_name='budgetsharemember',
            name='user_insert',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='user_insert_budgetsharemember', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='budgetsharemember',
            name='user_update',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_update_budgetsharemember', to=settings.AUTH_USER_MODEL),
        ),
    ]
