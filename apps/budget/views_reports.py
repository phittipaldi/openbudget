from django.http.response import HttpResponseForbidden
from django.views.generic import FormView, ListView
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
            object_list=data, resultados=[], form=form)
        return self.render_to_response(context)

    def filter_data(self, budget, period):
        data = []

        for detail in budget.details.all():
            budget_data = BudgetData(budget, period,
                                     detail.category,
                                     detail.amount)
            data.append(budget_data)

        return data


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

        filter_data['account__in'] = self.budget.details.all().values(
            'accounts')
        filter_data['subcategory__category__in'] = [self.category]
        data = models.Transaction.objects.filter(**filter_data)
        data = data.values(
            'subcategory__category').annotate(
            amount=Sum('amount'))

        if len(data) > 0:
            return data[0]['amount']
        else:
            return 0

    def available(self):
        result = Decimal(self.budgeted) - self.activity()
        return result


class TransactionDetails(ListView):
    model = models.Transaction
    template_name = 'modals/content_transaction_details.html'
    paginate_by = 5

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
        category = models.Category.objects.get(
            pk=int(self.kwargs['category']))
        period = models.BudgetPeriod.objects.get(
            pk=int(self.kwargs['period']))
        return self.model.objects.my_transactions_by_period(
            self.request.user, category, period)
