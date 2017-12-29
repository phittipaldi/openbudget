# from django.urls.base import reverse
# from django.conf import settings
# from django.http import Http404
from django.views.generic.list import ListView
# from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import (LoginRequiredMixin)
from .models import Transaction
# from .forms import AccountTransactionForm, AccountTransactionUpdateForm
# from apps.utils.models import Currency


class TransactionList(LoginRequiredMixin, ListView):
    template_name = "transaction_list.html"
    model = Transaction
    context_object_name = 'transactions'

    def get_context_data(self, **kwargs):
        context = super(TransactionList, self).get_context_data(**kwargs)
        return context

    # def get_queryset(self):
    #     return self.model.objects.all_my_accounts(self.request.user)
