from django.urls.base import reverse
from django.conf import settings
from django.http import Http404
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import (LoginRequiredMixin)
from .models import Account, AccountType
from .forms import AccountTransactionForm, AccountTransactionUpdateForm
from apps.utils.models import Currency


class AccountList(LoginRequiredMixin, ListView):
    template_name = "account_list.html"
    model = Account
    context_object_name = 'accounts'

    def get_context_data(self, **kwargs):
        context = super(AccountList, self).get_context_data(**kwargs)
        return context

    def get_queryset(self):
        return self.model.objects.all_my_accounts(self.request.user)


class AccountAdd(LoginRequiredMixin, CreateView):
    template_name = "account_add.html"
    model = Account
    form_class = AccountTransactionForm
    login_url = settings.LOGIN_URL

    def get_context_data(self, **kwargs):
        context = super(AccountAdd, self).get_context_data(**kwargs)
        context['form'].fields['currency'].queryset = self.get_my_currencies()
        return context

    def form_valid(self, form):
        form.instance.user_insert = self.request.user
        form.save()
        form.instance.owners.add(self.request.user)
        return super(AccountAdd, self).form_valid(form)

    def get_success_url(self):
        return reverse('budget:account_list')

    def get_my_currencies(self):
        choices = Currency.objects.all_my_currencies(self.request.user)
        return choices

    def get_ac_types(self):
        choices = [(o.id, str(o)) for o in AccountType.objects.all()]
        return choices


class AccountUpdate(LoginRequiredMixin, UpdateView):
    template_name = "account_update.html"
    model = Account
    form_class = AccountTransactionUpdateForm
    login_url = settings.LOGIN_URL

    def form_valid(self, form):
        form.instance.user_update = self.request.user
        return super(AccountUpdate, self).form_valid(form)

    def get_success_url(self):
        return reverse('budget:account_list')

    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        obj = super(AccountUpdate, self).get_object()
        if not obj.owners.filter(username__in=[
                                 self.request.user]).count():
            raise Http404
        return obj


class AccountDelete(LoginRequiredMixin, DeleteView):
    template_name = "account_delete.html"
    model = Account
    form_class = AccountTransactionUpdateForm
    login_url = settings.LOGIN_URL

    def get_success_url(self):
        return reverse('budget:account_list')

    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        obj = super(AccountDelete, self).get_object()
        if not obj.owners.filter(username__in=[
                                 self.request.user]).count():
            raise Http404
        return obj
