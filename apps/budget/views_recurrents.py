from django.views.generic import (CreateView, ListView, UpdateView,
                                  View, DeleteView)
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import (RecurrentTransaction, TransactionType, RecurrentShedule,
                     DayShedule, SubCategory, Account, Category)
from apps.utils.models import Currency
from .forms import RecurrentTransactionForm, RecurrentSheduleForm
from django.conf import settings
from django.urls.base import reverse
from django.http.response import JsonResponse
from django.http import Http404


class RecurrentList(LoginRequiredMixin, ListView):
    template_name = "recurrent_trx_list.html"
    model = RecurrentTransaction
    login_url = settings.LOGIN_URL

    def get_queryset(self):
        return self.model.objects.all_my_recurrents(self.request.user)


class RecurrentDelete(LoginRequiredMixin, DeleteView):
    template_name = "recurrent_delete.html"
    model = RecurrentTransaction
    form_class = RecurrentTransactionForm
    login_url = settings.LOGIN_URL

    def get_success_url(self):
        return reverse('budget:setting_recurrent')

    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        obj = super(RecurrentDelete, self).get_object()
        if not obj.user_insert == self.request.user:
            raise Http404
        return obj


class RecurrentCreate(LoginRequiredMixin, CreateView):
    template_name = "recurrent_trx_create.html"
    model = RecurrentTransaction
    form_class = RecurrentTransactionForm
    login_url = settings.LOGIN_URL

    def get_context_data(self, **kwargs):
        context = super(RecurrentCreate, self).get_context_data(**kwargs)
        context['form'].fields['currency'].queryset = self.get_my_currencies()
        context['form'].fields['account'].queryset = self.get_my_accounts()
        empty_query = SubCategory.objects.none()
        context['form'].fields['category'].queryset = empty_query
        context['form'].fields['subcategory'].queryset = empty_query
        return context

    def post(self, request, *args, **kwargs):
        return super(RecurrentCreate, self).post(request)

    def form_valid(self, form):
        form.instance.user_insert = self.request.user
        form.instance.trx_type = TransactionType.objects.get(pk=1)
        form.instance.exchange = 1
        form.save()
        form.instance.shedule.create()
        return super(RecurrentCreate, self).form_valid(form)

    def get_success_url(self):
        recurrent_shedule = self.object.shedule.all()[0]
        return reverse('budget:setting_recurrent_shedule',
                       kwargs={'pk': recurrent_shedule.pk})

    def get_my_currencies(self):
        choices = Currency.objects.all_my_currencies(self.request.user)
        return choices

    def get_my_accounts(self):
        choices = Account.objects.all_my_accounts(self.request.user)
        return choices


class RecurrentUpdate(LoginRequiredMixin, UpdateView):
    template_name = "recurrent_trx_create.html"
    model = RecurrentTransaction
    form_class = RecurrentTransactionForm
    login_url = settings.LOGIN_URL

    def get_context_data(self, **kwargs):
        context = super(RecurrentUpdate, self).get_context_data(**kwargs)
        context['form'].fields['account'].queryset = self.get_my_accounts()
        context['form'].fields['currency'].queryset = self.get_my_currencies()
        context['form'].fields[
            'category'].queryset = Category.objects.all_my_categories(
                self.request.user)
        context['form'].fields[
            'subcategory'].queryset = SubCategory.objects.filter(
                category__id=self.get_object().subcategory.category.pk)
        context['form'].fields[
            'category'].initial = self.get_object().subcategory.category.pk
        return context

    def form_valid(self, form):
        form.instance.user_update = self.request.user
        form.instance.trx_type = TransactionType.objects.get(pk=1)
        form.instance.exchange = 1
        form.save()
        return super(RecurrentUpdate, self).form_valid(form)

    def get_success_url(self):
        recurrent_shedule = self.object.shedule.all()[0]
        return reverse('budget:setting_recurrent_shedule',
                       kwargs={'pk': recurrent_shedule.pk})

    def get_my_currencies(self):
        choices = Currency.objects.all_my_currencies(self.request.user)
        return choices

    def get_my_accounts(self):
        choices = Account.objects.all_my_accounts(self.request.user)
        return choices


class RecurrentSetShedule(LoginRequiredMixin, UpdateView):
    template_name = "recurrent_shedule.html"
    model = RecurrentShedule
    form_class = RecurrentSheduleForm
    login_url = settings.LOGIN_URL

    def get_context_data(self, **kwargs):
        context = super(RecurrentSetShedule, self).get_context_data(**kwargs)

        try:
            context['form'].fields[
                'period_type'].initial = self.get_object().day.period_type.pk
        except Exception:
            pass

        return context

    def form_valid(self, form):
        if self.get_object().lines.count() == 0:
            form.instance.set_next_shedule_line()
        return super(RecurrentSetShedule, self).form_valid(form)

    def get_success_url(self):
        return reverse('budget:setting_recurrent')

    def get_form(self, form_class=None):
        form = super(RecurrentSetShedule, self).get_form(form_class)
        if self.get_object().lines.count() > 0:
            form.fields['period_type'].widget.attrs.update(
                {'readonly': 'true'})
            form.fields['day'].widget.attrs.update({'readonly': 'true'})
            form.fields['start_posting'].widget.attrs.update(
                {'readonly': 'true'})
        return form


class DaySheduleView(View):
    model = DayShedule

    def get(self, request, *args, **kwargs):

        objects = self.model.objects.filter(
            period_type__id=self.kwargs.get('period_type'))

        result = []
        for i in objects:
            result.append({"id": i.pk, "name": i.name})

        return JsonResponse(result, safe=False)
