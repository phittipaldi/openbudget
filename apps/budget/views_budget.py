from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls.base import reverse
from django.views.generic import CreateView, ListView, UpdateView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import (LoginRequiredMixin)
from .forms import BudgetForm
from .models import Budget, Category, BudgetLine, BudgetPeriod


class BudgetDetail(LoginRequiredMixin, DetailView):
    template_name = "budget_detail.html"
    model = Budget


class BudgetCreate(LoginRequiredMixin, CreateView):
    template_name = "budget_create.html"
    model = Budget
    form_class = BudgetForm
    login_url = settings.LOGIN_URL

    def get_context_data(self, **kwargs):
        context = super(BudgetCreate, self).get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        form.instance.user_insert = self.request.user
        form.save()
        return HttpResponseRedirect(
            reverse('budget:budget_global_details',
                    kwargs={'budget_pk': form.instance.pk}))


class BudgetUpdate(LoginRequiredMixin, UpdateView):
    template_name = "budget_create.html"
    model = Budget
    form_class = BudgetForm
    login_url = settings.LOGIN_URL

    def get_context_data(self, **kwargs):
        context = super(BudgetUpdate, self).get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        form.instance.user_insert = self.request.user
        form.save()
        return HttpResponseRedirect(
            reverse('budget:budget_global_details',
                    kwargs={'budget_pk': form.instance.pk}))


class BudgetDetailGlobal(LoginRequiredMixin, ListView):
    template_name = "budget_detail_global.html"
    model = BudgetLine

    def get_context_data(self, **kwargs):
        context = super(BudgetDetailGlobal, self).get_context_data(**kwargs)
        context['budget'] = Budget.objects.get(pk=self.kwargs.get('budget_pk'))
        return context

    def post(self, request, *args, **kwargs):
        budget = Budget.objects.get(pk=kwargs.get('budget_pk'))
        budget_g = BudgetGlobalAmount(budget)
        budget_g.set_global_values(request.POST)
        return HttpResponseRedirect(reverse('budget:detail',
                                    kwargs={'pk': kwargs.get('budget_pk')}))

    def get_queryset(self):
        budget = Budget.objects.get(pk=self.kwargs.get('budget_pk'))
        BudgetGlobalAmount.set_global_lines(budget)
        first_period = BudgetPeriod.objects.filter(
            budget__pk=budget.pk).first()
        queryset = self.model.objects.select_related(
            'subcategory', 'subcategory__category').filter(
            period__pk=first_period.pk)
        return queryset


class BudgetGlobalAmount:

    def __init__(self, budget):
        self.budget = budget

    @classmethod
    def set_global_lines(self, budget):

        categories = Category.objects.filter(user_insert=budget.user_insert)

        for period in budget.periods.all()[:1]:

            for category in categories:

                for subcategory in category.subcategories.all():

                    BudgetLine.objects.get_or_create(period=period,
                                                     subcategory=subcategory)

    def set_global_values(self, postlist):
        for period in self.budget.periods.all():
            for line in period.details.all():
                line.amount = postlist.get(str(line.pk))
                line.save()
