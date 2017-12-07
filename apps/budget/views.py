from django.views.generic.list import ListView
from .models import Account


class AccountList(ListView):
    template_name = "account_list.html"
    model = Account
    context_object_name = 'accounts'

    def get_context_data(self, **kwargs):
        context = super(AccountList, self).get_context_data(**kwargs)
        return context
