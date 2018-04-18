# -*- coding: utf-8 -*-
from django.views.generic import TemplateView
from django.contrib.auth.mixins import (LoginRequiredMixin)
from apps.budget.forms import BudgetReportForm
from django.views.generic import FormView
from apps.budget import models
import datetime


# class HomePage(LoginRequiredMixin, TemplateView):
#     template_name = "dashboard_old.html"


# class DashboardPage(LoginRequiredMixin, TemplateView):
#     template_name = "dashboard_old.html"


class DashboardPage(LoginRequiredMixin, FormView):
    template_name = "dashboard.html"
    form_class = BudgetReportForm

    def get_context_data(self, **kwargs):
        context = super(DashboardPage, self).get_context_data(**kwargs)
        my_budgets = self.get_my_budgets()
        context['form'].fields['budget'].queryset = my_budgets
        context['form'].fields['period'].queryset = my_budgets[0].periods

        context['form'].fields[
            'budget'].initial = my_budgets[0].pk

        context['form'].fields[
            'period'].initial = self.set_current_period(my_budgets[0])

        return context

    def get_my_budgets(self):
        choices = models.Budget.objects.all_my_budgets(self.request.user)
        return choices

    def set_current_period(self, budget):
        current_date = datetime.datetime.today()
        current_periods = budget.periods.filter(
            init_date__lte=current_date,
            end_date__gte=current_date)
        return current_periods[0]


class DashboardPageFilter(LoginRequiredMixin, FormView):
    template_name = "dashboard.html"
    form_class = BudgetReportForm

    def get_context_data(self, **kwargs):
        context = super(DashboardPageFilter, self).get_context_data(**kwargs)
        my_budgets = self.get_my_budgets()
        context['form'].fields['budget'].queryset = my_budgets
        context['form'].fields['period'].queryset = my_budgets[0].periods

        budget_selected = my_budgets.filter(pk=self.kwargs.get('budget'))[0]
        context['form'].fields[
            'budget'].initial = budget_selected

        context['form'].fields[
            'period'].initial = budget_selected.periods.filter(
                pk=self.kwargs.get('period'))[0]

        return context

    def get_my_budgets(self):
        choices = models.Budget.objects.all_my_budgets(self.request.user)
        return choices
