from django.views.generic import FormView
from .forms import BudgetReportForm
from . import models
from django.db.models import Sum
from decimal import Decimal


class BudgetReport(FormView):
    template_name = 'budget_report.html'
    form_class = BudgetReportForm
    model = models.Transaction

    def get(self, request, *args, **kwargs):
        if request.GET.items():
            form = self.form_class(self.request.GET)
            if form.is_valid():
                return self.get_data_report(form)

        return self.render_to_response(self.get_context_data())

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
