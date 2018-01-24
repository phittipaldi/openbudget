# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-16 15:24
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('budget', '0010_currencyuser_owner'),
    ]

    operations = [
        migrations.CreateModel(
            name='Budget',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BudgetDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('accounts', models.ManyToManyField(to='budget.Account')),
                ('budget', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='budget.Budget')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='budget.Category')),
            ],
        ),
        migrations.CreateModel(
            name='BudgetPeriod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=128)),
                ('init_date', models.DateField()),
                ('end_date', models.DateField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PeriodType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
            ],
        ),
        migrations.AddField(
            model_name='budgetperiod',
            name='period_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='budget.PeriodType'),
        ),
        migrations.AddField(
            model_name='budgetperiod',
            name='user_insert',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_insert_budgetperiod', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='budgetperiod',
            name='user_update',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_update_budgetperiod', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='budget',
            name='period_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='budget.PeriodType'),
        ),
        migrations.AddField(
            model_name='budget',
            name='user_insert',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_insert_budget', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='budget',
            name='user_update',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_update_budget', to=settings.AUTH_USER_MODEL),
        ),
    ]