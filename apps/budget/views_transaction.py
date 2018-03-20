from django.urls.base import reverse
from django.contrib import messages
from django.conf import settings
from django.http import Http404
from django.views.generic.list import ListView
from django.views.generic.edit import (CreateView, View, UpdateView,
                                       DeleteView)
from django.http.response import JsonResponse
from django.contrib.auth.mixins import (LoginRequiredMixin)
from .models import (Transaction, Account, SubCategory,
                     TransactionType, DurationFilter, Category)
from .forms import TransactionForm
from apps.utils.models import Currency


class TransactionList(LoginRequiredMixin, ListView):
    template_name = "transaction_list.html"
    model = Transaction
    context_object_name = 'transactions'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(TransactionList, self).get_context_data(**kwargs)
        context['duration_filter'] = DurationFilter.objects.all()
        if 'duration' in self.kwargs:
            context['current_duration'] = int(self.kwargs.get('duration'))
        return context

    def get_queryset(self):
        if 'duration' not in self.kwargs:
            return self.model.objects.last_30_days_transactions(
                self.request.user)
        else:
            return self.model.objects.transactions_by_duration(
                self.request.user, self.kwargs['duration'])


class TransactionAdd(LoginRequiredMixin, CreateView):
    template_name = "transaction_add.html"
    form_class = TransactionForm
    model = Transaction
    login_url = settings.LOGIN_URL
    success_url = 'budget:transaction_list'

    def get_context_data(self, **kwargs):
        context = super(TransactionAdd, self).get_context_data(**kwargs)
        context['form'].fields['currency'].queryset = self.get_my_currencies()
        context['form'].fields['account'].queryset = self.get_my_accounts()
        empty_query = SubCategory.objects.none()
        context['form'].fields['category'].queryset = empty_query
        context['form'].fields['subcategory'].queryset = empty_query
        return context

    def form_valid(self, form):
        form.instance.user_insert = self.request.user
        form.instance.trx_type = TransactionType.objects.get(pk=1)
        form.instance.exchange = 1
        form.save()

        if "_continue" in self.request.POST:
            self.success_url = "budget:transaction_add"
            message = self.save_and_continue_string(form.instance)
            messages.success(self.request, message)

        return super(TransactionAdd, self).form_valid(form)

    def form_invalid(self, form):
        return super(TransactionAdd, self).form_invalid(form)

    def get_success_url(self):
        return reverse(self.success_url)

    def save_and_continue_string(self, instance):
        return 'The transaction "{1}" was added successfully. '\
               'You may add another {0}'.format(instance._meta.object_name,
                                                instance)

    def get_my_currencies(self):
        choices = Currency.objects.all_my_currencies(self.request.user)
        return choices

    def get_my_accounts(self):
        choices = Account.objects.all_my_accounts(self.request.user)
        return choices


class TransactionUpdate(LoginRequiredMixin, UpdateView):
    template_name = "transaction_update.html"
    form_class = TransactionForm
    model = Transaction
    login_url = settings.LOGIN_URL

    def get_context_data(self, **kwargs):
        context = super(TransactionUpdate, self).get_context_data(**kwargs)
        context['form'].fields['currency'].queryset = self.get_my_currencies()
        context['form'].fields['account'].queryset = self.get_my_accounts()
        context['form'].fields[
            'subcategory'].queryset = SubCategory.objects.filter(
                category__id=self.get_object().subcategory.category.pk)
        context['form'].fields[
            'category'].initial = self.get_object().subcategory.category.pk
        return context

    def form_valid(self, form):
        form.instance.user_update = self.request.user
        form.save()
        return super(TransactionUpdate, self).form_valid(form)

    def form_invalid(self, form):
        return super(TransactionUpdate, self).form_valid(form)

    def get_success_url(self):
        return reverse('budget:transaction_list')

    def get_my_currencies(self):
        choices = Currency.objects.all_my_currencies(self.request.user)
        return choices

    def get_my_accounts(self):
        choices = Account.objects.all_my_accounts(self.request.user)
        return choices


class TransactionDelete(LoginRequiredMixin, DeleteView):
    template_name = "transaction_delete.html"
    model = Transaction
    form_class = TransactionForm
    login_url = settings.LOGIN_URL

    def get_success_url(self):
        return reverse('budget:transaction_list')

    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        obj = super(TransactionDelete, self).get_object()
        if not obj.account.owners.filter(username__in=[
                                         self.request.user]).count():
            raise Http404
        return obj


class CategoryView(View):
    model = Category

    def get(self, request, *args, **kwargs):
        account = Account.objects.get(
            id=self.kwargs.get('account_pk'))
        objects = self.model.objects.filter(
            user_insert__id=account.user_insert.pk)

        result = []
        for i in objects:
            result.append({"id": i.pk, "name": i.name})

        return JsonResponse(result, safe=False)


class SubCategoryView(View):
    model = SubCategory

    def get(self, request, *args, **kwargs):

        objects = self.model.objects.filter(
            category__id=self.kwargs.get('category'))

        result = []
        for i in objects:
            result.append({"id": i.pk, "name": i.name})

        return JsonResponse(result, safe=False)
