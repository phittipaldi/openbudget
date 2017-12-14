from django.urls.base import reverse
from django.conf import settings
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import (LoginRequiredMixin)
from .models import Account
from .forms import AccountTransactionForm


class AccountList(ListView):
    template_name = "account_list.html"
    model = Account
    context_object_name = 'accounts'

    def get_context_data(self, **kwargs):
        context = super(AccountList, self).get_context_data(**kwargs)
        return context


class AccountAdd(LoginRequiredMixin, CreateView):
    template_name = "account_add.html"
    model = Account
    form_class = AccountTransactionForm
    login_url = settings.LOGIN_URL

    def get_context_data(self, **kwargs):
        context = super(AccountAdd, self).get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        form.instance.user_insert = self.request.user
        return super(AccountAdd, self).form_valid(form)

    def get_success_url(self):
        return reverse('budget:account_list')
