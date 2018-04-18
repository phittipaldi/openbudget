from django.http.response import HttpResponseForbidden
from django.http.response import JsonResponse
from django.views.generic import FormView, ListView
from django.views.generic.edit import View
from .forms import BudgetReportForm
from . import models
from django.db.models import Sum
from decimal import Decimal


class BudgetReport(FormView):
    template_name = 'budget_report.html'
    form_class = BudgetReportForm
    model = models.Transaction

    def get_context_data(self, **kwargs):
        context = super(BudgetReport, self).get_context_data(**kwargs)
        context['form'].fields['budget'].queryset = self.get_my_budgets()

        return context

    def get(self, request, *args, **kwargs):
        if request.GET.items():
            form = self.form_class(self.request.GET)
            if form.is_valid():
                return self.get_data_report(form)

        return self.render_to_response(self.get_context_data())

    def get_my_budgets(self):
        choices = models.Budget.objects.all_my_budgets(self.request.user)
        return choices

    def form_valid(self, form):
        budget = form.cleaned_data.get('budget')
        period = form.cleaned_data.get('period')
        data = self.filter_data(budget, period)
        context = self.get_context_data(
            object_list=data, budget=budget, period=period, form=form)
        context['form'].fields[
            'period'].queryset = models.BudgetPeriod.objects.filter(
            budget__pk=budget.pk)
        return self.render_to_response(context)

    def filter_data(self, budget, period):
        data = []
        details = period.details.values(
            'subcategory__category').annotate(
            amount=Sum('amount'))
        for detail in details.all():
            category = models.Category.objects.get(
                pk=detail['subcategory__category'])
            budget_data = BudgetData(budget, period,
                                     category,
                                     detail['amount'])
            data.append(budget_data)

        return data


class BudgetPeriodView(View):
    model = models.BudgetPeriod

    def get(self, request, *args, **kwargs):

        objects = self.model.objects.filter(
            budget__id=self.kwargs.get('budget'))

        result = []
        for i in objects:
            result.append({"id": i.pk, "name": i.description})

        return JsonResponse(result, safe=False)


class BudgetData:

    def __init__(self, budget, period, category, amount_budget):
        self.budget = budget
        self.period = period
        self.category = category
        self.budgeted = amount_budget

    def activity(self):
        filter_data = dict()
        filter_data['date__range'] = [self.period.init_date,
                                      self.period.end_date]

        filter_data['account__in'] = self.budget.accounts.all()
        filter_data['subcategory__category__in'] = [self.category]
        data = models.Transaction.objects.filter(**filter_data)
        data = data.values(
            'subcategory__category').annotate(
            amount_account=Sum('amount_account'))

        if len(data) > 0:
            return data[0]['amount_account']
        else:
            return 0

    def available(self):
        result = Decimal(self.budgeted) - self.activity()
        return result


class BudgetbySubcategories(ListView):
    model = models.Transaction
    template_name = 'budget_report_subcategories.html'

    def get_context_data(self, **kwargs):
        context = super(BudgetbySubcategories, self).get_context_data(**kwargs)
        context['category'] = models.Category.objects.get(
            pk=int(self.kwargs['category']))
        context['period'] = models.BudgetPeriod.objects.get(
            pk=int(self.kwargs['period']))
        return context

    def get_queryset(self):
        budget = models.Budget.objects.get(
            pk=int(self.kwargs['budget']))
        category = models.Category.objects.get(
            pk=int(self.kwargs['category']))
        period = models.BudgetPeriod.objects.get(
            pk=int(self.kwargs['period']))
        data = self.filter_data(budget, period, category)
        return data

    def filter_data(self, budget, period, category):
        data = []
        details = period.details.filter(
            subcategory__category__pk=category.pk)
        for detail in details.all():
            budget_data = BudgetSubData(budget, period,
                                        detail.subcategory,
                                        detail.amount)
            data.append(budget_data)

        return data


class BudgetSubData:

    def __init__(self, budget, period, subcategory, amount_budget):
        self.budget = budget
        self.period = period
        self.subcategory = subcategory
        self.budgeted = amount_budget

    def activity(self):
        filter_data = dict()
        filter_data['date__range'] = [self.period.init_date,
                                      self.period.end_date]

        filter_data['account__in'] = self.budget.accounts.all()
        filter_data['subcategory__in'] = [self.subcategory]
        data = models.Transaction.objects.filter(**filter_data)
        data = data.values(
            'subcategory').annotate(
            amount_account=Sum('amount_account'))

        if len(data) > 0:
            return data[0]['amount_account']
        else:
            return 0

    def available(self):
        result = Decimal(self.budgeted) - self.activity()
        return result


class TransactionDetails(ListView):
    model = models.Transaction
    template_name = 'modals/content_transaction_details.html'

    def __init__(self, *args, **kwargs):
        super(TransactionDetails, self).__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(TransactionDetails, self).get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        response = super(TransactionDetails, self).get(
            request, *args, **kwargs)
        if self.request.is_ajax():
            return response
        return HttpResponseForbidden()

    def get_queryset(self):
        subcategory = models.SubCategory.objects.get(
            pk=int(self.kwargs['subcategory']))
        period = models.BudgetPeriod.objects.get(
            pk=int(self.kwargs['period']))
        return self.model.objects.my_transactions_by_subcategory(
            self.request.user, subcategory, period)
