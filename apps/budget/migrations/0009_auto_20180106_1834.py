# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-06 18:34
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0008_iconcategory_css'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='user_insert',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_insert_account', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='currencyuser',
            name='user_insert',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_insert_currencyuser', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='subcategory',
            name='user_insert',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_insert_subcategory', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='user_insert',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_insert_transaction', to=settings.AUTH_USER_MODEL),
        ),
    ]