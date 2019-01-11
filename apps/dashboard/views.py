# -*- coding: utf-8 -*-
from django.contrib.auth.mixins import (LoginRequiredMixin)
from apps.budget.forms import BudgetReportForm
from django.views.generic import FormView, RedirectView
from apps.budget import models
import datetime
from django.urls import reverse


class DashboardRedirect(LoginRequiredMixin, RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        budgets = models.Budget.objects.all_my_budgets(
            self.request.user)

        if budgets.count() > 0:
            url = reverse('dashboard')
        else:
            url = reverse('budget:list')
        return url


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
        current_date = datetime.datetime.today()
        choices = models.Budget.objects.all_my_budgets(self.request.user)
        choices = choices.filter(year__value=current_date.year.real)
        return choices

    def set_current_period(self, budget):
        current_date = datetime.datetime.today()
        current_periods = budget.periods.filter(
            init_date__lte=current_date,
            end_date__gte=current_date)

        if current_periods.count() > 0:
            return current_periods[0]


class DashboardPageFilter(LoginRequiredMixin, FormView):
    template_name = "dashboard.html"
    form_class = BudgetReportForm

    def get_context_data(self, **kwargs):
        context = super(DashboardPageFilter, self).get_context_data(**kwargs)
        my_budgets = self.get_my_budgets()
        budget_selected = my_budgets.filter(pk=self.kwargs.get('budget'))[0]

        context['form'].fields['budget'].queryset = my_budgets
        context['form'].fields['period'].queryset = budget_selected.periods

        context['form'].fields[
            'budget'].initial = budget_selected

        context['form'].fields[
            'period'].initial = budget_selected.periods.filter(
                pk=self.kwargs.get('period'))[0]

        return context

    def get_my_budgets(self):
        choices = models.Budget.objects.all_my_budgets(self.request.user)
        return choices
