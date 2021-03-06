# # -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.response import Response
from rest_framework.views import APIView
from apps.budget import models
from apps.budget import views_reports
from django.db.models import Sum
from rest_framework.authentication import (SessionAuthentication,
                                           BasicAuthentication
                                           )


class DataBudget(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = []

    def get(self, request, **kwargs):
        queryset = self.filter_data(kwargs)
        labels = self.set_labels(queryset)
        default_items = self.set_defaults(queryset, kwargs)
        bg_colors = self.set_bg_colors(queryset)
        ln_colors = self.set_ln_colors(queryset)
        data = {
            "labels": labels,
            "default": default_items,
            "bg_colors": bg_colors,
            "ln_colors": ln_colors
        }

        return Response(data)

    def set_labels(self, queryset):
        labels = []
        for item in queryset:
            category = models.Category.objects.get(
                pk=item['subcategory__category'])
            labels.append(category.name)

        return labels

    def set_defaults(self, queryset, kwargs):
        default_items = []
        for item in queryset:
            category = models.Category.objects.get(
                pk=item['subcategory__category'])
            period = models.BudgetPeriod.objects.get(
                pk=kwargs['period'])

            budget_data = views_reports.BudgetData(
                period.budget, period, category, item['amount'])
            data_percent = self.get_percent(budget_data)
            default_items.append(data_percent)

        return default_items

    def get_percent(self, budget_data):
        result = 0

        try:
            result = (budget_data.activity() / budget_data.budgeted) * 100
        except Exception:
            result = budget_data.activity()

        return result

    def filter_data(self, kwargs):
        period = models.BudgetPeriod.objects.get(
            pk=kwargs['period'])
        queryset = period.details.values(
            'subcategory__category').annotate(
            amount=Sum('amount'))

        return queryset

    def set_bg_colors(self, queryset):
        bg_colors = []
        for item in queryset:
            category = models.Category.objects.get(
                pk=item['subcategory__category'])
            bg_colors.append(category.icon.color.bg_code)

        return bg_colors

    def set_ln_colors(self, queryset):
        ln_colors = []
        for item in queryset:
            category = models.Category.objects.get(
                pk=item['subcategory__category'])
            ln_colors.append(category.icon.color.border_code)

        return ln_colors


class DataBudgetActivity(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = []

    def get(self, request, **kwargs):
        queryset = self.filter_data(kwargs)
        data, totals = self.set_defaults(queryset, kwargs)
        data_json = {'data': data, 'totals': totals}
        return Response(data_json)

    def set_defaults(self, queryset, kwargs):
        default_items = []
        budgeted = 0
        activity = 0
        available = 0
        for item in queryset:
            category = models.Category.objects.get(
                pk=item['subcategory__category'])
            period = models.BudgetPeriod.objects.get(
                pk=kwargs['period'])

            budget_data = views_reports.BudgetData(
                period.budget, period, category, item['amount'])

            default_item = dict(category=budget_data.category.name,
                                budgeted='{:,}'.format(budget_data.budgeted),
                                activity='{:,}'.format(budget_data.activity()),
                                available='{:,}'.format(
                                    budget_data.available()),
                                icon=budget_data.category.icon.css,
                                color=budget_data.category.icon.color.css,
                                currency=period.budget.currency.name)

            default_items.append(default_item)

            budgeted = budgeted + budget_data.budgeted
            activity = activity + budget_data.activity()
            available = available + budget_data.available()

        totals = {'budgeted': '{:,}'.format(budgeted),
                  'activity': '{:,}'.format(activity),
                  'available': '{:,}'.format(available)}

        return default_items, totals

    def filter_data(self, kwargs):
        period = models.BudgetPeriod.objects.get(
            pk=kwargs['period'])
        queryset = period.details.values(
            'subcategory__category').annotate(
            amount=Sum('amount'))

        return queryset
