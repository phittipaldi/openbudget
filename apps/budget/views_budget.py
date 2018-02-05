from django.conf import settings
from django.http import HttpResponseRedirect
from django.http import Http404
from django.urls.base import reverse
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import (LoginRequiredMixin)
from .forms import BudgetForm
from .models import Budget, Category, BudgetLine, BudgetPeriod
import threading
from django.db.models import Sum


class BudgetList(LoginRequiredMixin, ListView):
    template_name = "budget_list.html"
    model = Budget

    def get_queryset(self):
        return self.model.objects.all_my_budgets(self.request.user)


class BudgetDelete(LoginRequiredMixin, DeleteView):
    template_name = "budget_delete.html"
    model = Budget
    form_class = BudgetForm
    login_url = settings.LOGIN_URL

    def get_success_url(self):
        return reverse('budget:list')

    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        obj = super(BudgetDelete, self).get_object()
        if not obj.owners.filter(username__in=[
                                 self.request.user]).count():
            raise Http404
        return obj


class BudgetDetail(LoginRequiredMixin, DetailView):
    template_name = "budget_detail.html"
    model = Budget

    def get_context_data(self, **kwargs):
        context = super(BudgetDetail, self).get_context_data(**kwargs)
        context['object_list'] = self.get_budget_resume()
        return context

    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        obj = super(BudgetDetail, self).get_object()
        if not obj.user_insert == self.request.user:
            raise Http404

        return obj

    def get_budget_resume(self):
        budget = super(BudgetDetail, self).get_object()
        period = budget.periods.first()
        details = period.details.values(
            'subcategory__category__name').annotate(amount=Sum('amount'))
        return details


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
        form.instance.owners.add(self.request.user)
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

    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        obj = super(BudgetUpdate, self).get_object()
        if not obj.user_insert == self.request.user:
            raise Http404
        return obj


class BudgetDetailGlobal(LoginRequiredMixin, ListView):
    template_name = "budget_detail_global.html"
    model = BudgetLine

    def get_context_data(self, **kwargs):
        context = super(BudgetDetailGlobal, self).get_context_data(**kwargs)
        context['budget'] = Budget.objects.get(pk=self.kwargs.get('budget_pk'))
        return context

    def post(self, request, *args, **kwargs):
        budget = Budget.objects.get(pk=kwargs.get('budget_pk'))
        BudgetGlobalThread(budget, request.POST).start()
        return HttpResponseRedirect(reverse('budget:detail',
                                    kwargs={'pk': kwargs.get('budget_pk')}))

    def get_queryset(self):
        budget = Budget.objects.get(pk=self.kwargs.get('budget_pk'))
        budget_global = BudgetGlobalAmount(budget)
        budget_global.set_first_period_lines()
        first_period = BudgetPeriod.objects.filter(
            budget__pk=budget.pk).first()
        queryset = self.model.objects.select_related(
            'subcategory', 'subcategory__category').filter(
            period__pk=first_period.pk)
        return queryset


class BudgetGlobalAmount:

    def __init__(self, budget):
        self.budget = budget

    def set_first_period_lines(self):

        for period in self.budget.periods.all()[:1]:
            self.set_lines_budget(period)

    def set_lines_budget(self, period):
        categories = Category.objects.filter(
            user_insert=self.budget.user_insert)
        for category in categories:

            for subcategory in category.subcategories.all():

                BudgetLine.objects.get_or_create(period=period,
                                                 subcategory=subcategory)


class BudgetGlobalThread(threading.Thread, BudgetGlobalAmount):

    def __init__(self, budget, postlist):
        BudgetGlobalAmount.__init__(self, budget)
        self.postlist = postlist
        threading.Thread.__init__(self)

    def run(self):
        for period in self.budget.periods.all():

            if len(period.details.all()) == 0:
                self.set_lines_budget(period)

            for line in period.details.all():
                line.amount = self.postlist.get(line.subcategory.name)
                line.save()
