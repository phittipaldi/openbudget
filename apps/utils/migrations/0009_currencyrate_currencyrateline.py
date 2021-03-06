# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-02-08 08:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0008_auto_20180207_1929'),
    ]

    operations = [
        migrations.CreateModel(
            name='CurrencyRate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='utils.Currency')),
            ],
        ),
        migrations.CreateModel(
            name='CurrencyRateLine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.DecimalField(decimal_places=2, max_digits=10)),
                ('quote', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='utils.Currency')),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quotes', to='utils.CurrencyRate')),
            ],
        ),
    ]
