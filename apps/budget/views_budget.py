from django.conf import settings
from django.urls.base import reverse
from django.views.generic.edit import CreateView
from django.views.generic import TemplateView
from django.contrib.auth.mixins import (LoginRequiredMixin)
from .forms import BudgetForm
from .models import Budget


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
        return super(BudgetCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse('budget:budget_details')


class BudgetDetailCreate(LoginRequiredMixin, TemplateView):
    template_name = "budget_detail.html"
