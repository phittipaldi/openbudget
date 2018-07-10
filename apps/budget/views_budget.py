from django.conf import settings
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.http import Http404
from django.urls.base import reverse
from django.views.generic import (CreateView, ListView, UpdateView, DeleteView,
                                  FormView)
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import (LoginRequiredMixin)
from .forms import BudgetForm, BudgetShareForm, ShareConfirmationForm
from .models import (Budget, Category, BudgetLine, BudgetPeriod,
                     BudgetShareMember, BudgetShareStatus, CurrencyUser,
                     Account)
import threading
from django.db.models import Sum
from apps.utils.services import mail
from apps.utils.models import Currency
from django.conf import settings
from django.template.loader import render_to_string


class BudgetShareConfirmation(LoginRequiredMixin, UpdateView):
    template_name = "budget_share_confirmation.html"
    model = BudgetShareMember
    form_class = ShareConfirmationForm

    def form_valid(self, form):
        form.instance.status = BudgetShareStatus.objects.get(
            pk=2)
        form.save()
        self.extend_budget(form.instance)
        return super(BudgetShareConfirmation, self).form_valid(
            form)

    def get_success_url(self):
        return reverse('budget:list')

    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        obj = super(BudgetShareConfirmation, self).get_object()
        if not obj.member == self.request.user or not obj.status.pk == 1:
            raise Http404
        return obj

    def extend_budget(self, budget_share):
        # ---Budget---
        budget_share.budget.owners.add(budget_share.member)
        budget_share.budget.save()
        # ---Accounts---\
        for account in budget_share.budget.accounts.all():
            account.owners.add(budget_share.member)
            self.extend_currency(account)

    def extend_currency(self, account):

        if CurrencyUser.objects.filter(
                currency__pk=account.currency.pk,
                owner=self.request.user).count() == 0:
            origin = CurrencyUser.objects.get(currency__pk=account.currency.pk,
                                              user_insert=account.user_insert)
            CurrencyUser.objects.create(currency=origin.currency,
                                        owner=self.request.user,
                                        ratio=origin.ratio,
                                        inverse_ratio=origin.inverse_ratio,
                                        user_insert=origin.user_insert
                                        )


class BudgetShareCreate(LoginRequiredMixin, FormView):
    template_name = "budget_share_create.html"
    model = BudgetShareMember
    form_class = BudgetShareForm

    def get_context_data(self, **kwargs):
        context = super(BudgetShareCreate, self).get_context_data(**kwargs)
        context['budget'] = Budget.objects.get(pk=self.kwargs.get('budget_pk'))
        return context

    def form_valid(self, form):

        instance_created = self.create_share(form.cleaned_data['budget'])
        if instance_created:
            # Send notification
            self.send_share_notification(instance_created)
            return HttpResponseRedirect(self.get_success_url())
        else:
            return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('budget:budget_share_list',
                       kwargs={'budget_pk': self.kwargs.get('budget_pk')})

    def send_share_notification(self, budget_share):
        subject = 'Confirm Request Budget Sharing'
        html = render_to_string("mail/request_share_budget.html", {
                                'owner': budget_share.user_insert.first_name,
                                'member': budget_share.member,
                                'token': budget_share.token,
                                'current_domain': settings.CURRENT_DOMAIN})

        email = budget_share.member.email

        mail.send_html_mail(subject, html, [email])
        return True

    def create_share(self, email_user):
        try:
            share_user = User.objects.get(email=email_user)
            share_status = BudgetShareStatus.objects.get(pk=1)
            share_budget = Budget.objects.get(pk=self.kwargs.get('budget_pk'))
            instance = self.model.objects.create(
                member=share_user,
                budget=share_budget,
                status=share_status,
                user_insert=self.request.user)
        except User.DoesNotExist:
            instance = None

        return instance


class BudgetShareList(LoginRequiredMixin, ListView):
    template_name = "budget_share_list.html"
    model = BudgetShareMember

    def get_context_data(self, **kwargs):
        context = super(BudgetShareList, self).get_context_data(**kwargs)
        context['budget'] = Budget.objects.get(pk=self.kwargs.get('budget_pk'))
        return context

    def get_queryset(self):
        return self.model.objects.all_my_members_budget(
            self.request.user, self.kwargs.get('budget_pk'))


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


class BudgetList(LoginRequiredMixin, ListView):
    template_name = "budget_list.html"
    model = Budget

    def get_queryset(self):
        return self.model.objects.all_my_budgets(self.request.user)


class BudgetShareDelete(LoginRequiredMixin, DeleteView):
    template_name = "budget_share_delete.html"
    model = BudgetShareMember
    form_class = BudgetForm
    login_url = settings.LOGIN_URL

    def get_success_url(self):
        return reverse('budget:list')

    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        obj = super(BudgetShareDelete, self).get_object()
        if not obj.user_insert == self.request.user:
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
        context['form'].fields['currency'].queryset = self.get_my_currencies()
        empty_query = CurrencyUser.objects.none()
        context['form'].fields['accounts'].queryset = empty_query
        return context

    def form_valid(self, form):
        form.instance.user_insert = self.request.user
        form.save()
        form.instance.owners.add(self.request.user)
        return HttpResponseRedirect(
            reverse('budget:budget_global_details',
                    kwargs={'budget_pk': form.instance.pk}))

    def get_my_currencies(self):
        choices = Currency.objects.all_my_currencies(self.request.user)
        return choices


class BudgetUpdate(LoginRequiredMixin, UpdateView):
    template_name = "budget_create.html"
    model = Budget
    form_class = BudgetForm
    login_url = settings.LOGIN_URL

    def get_context_data(self, **kwargs):
        context = super(BudgetUpdate, self).get_context_data(**kwargs)
        context['form'].fields['currency'].queryset = self.get_my_currencies()
        context['form'].fields['accounts'].queryset = self.get_my_accounts()
        return context

    def form_valid(self, form):
        form.instance.user_insert = self.request.user
        self.remove_accounts_not_corresponding(form.instance)
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

    def get_my_currencies(self):
        choices = Currency.objects.all_my_currencies(self.request.user)
        return choices

    def get_my_accounts(self):
        budget = self.get_object()
        choices = Account.objects.all_my_accounts_currency(
            self.request.user, budget.currency.pk)
        return choices

    def remove_accounts_not_corresponding(self, budget):
        accounts = budget.accounts.filter().exclude(
            currency__pk=budget.currency.pk)

        for account in accounts:
            budget.accounts.remove(account)

        budget.save()


class BudgetDetailGlobal(LoginRequiredMixin, ListView):
    template_name = "budget_detail_global.html"
    model = BudgetLine

    def get_context_data(self, **kwargs):
        context = super(BudgetDetailGlobal, self).get_context_data(**kwargs)
        context['budget'] = Budget.objects.get(pk=self.kwargs.get('budget_pk'))
        return context

    def post(self, request, *args, **kwargs):
        budget = Budget.objects.get(pk=kwargs.get('budget_pk'))
        BudgetGlobal(budget, request.POST).register_first_amounts()
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

            # if len(period.details.all()) == 0:
            self.set_lines_budget(period)

            for line in period.details.all():
                amount_fixed = self.postlist.get(
                    line.subcategory.name).replace(',', '')
                line.amount = amount_fixed
                line.save()


class BudgetGlobal(BudgetGlobalAmount):

    def __init__(self, budget, postlist):
        BudgetGlobalAmount.__init__(self, budget)
        self.postlist = postlist

    def register_first_amounts(self):

        for period in self.budget.periods.all()[:1]:
            if len(period.details.all()) == 0:
                self.set_lines_budget(period)

            for line in period.details.all():
                amount_fixed = self.postlist.get(
                    line.subcategory.name).replace(',', '')
                line.amount = amount_fixed
                line.save()
