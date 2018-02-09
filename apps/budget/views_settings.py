from django.urls.base import reverse
from django.http import Http404
from django.views.generic import (ListView, CreateView, UpdateView,
                                  DeleteView)
from django.contrib.auth.mixins import (LoginRequiredMixin)
from apps.budget import models
from apps.utils.models import Currency
from .forms import SubcategoryForm, CurrencyUserForm


class SettingCurrency(LoginRequiredMixin, ListView):
    template_name = "setting_currency.html"
    model = models.CurrencyUser

    def get_queryset(self):
        queryset = self.model.objects.all_my_currencies(self.request.user)
        return queryset


class SettingCurrencyAdd(LoginRequiredMixin, CreateView):
    template_name = "setting_currency_add.html"
    model = models.CurrencyUser
    form_class = CurrencyUserForm

    def get_context_data(self, **kwargs):
        context = super(SettingCurrencyAdd, self).get_context_data(**kwargs)
        context['form'].fields[
            'currency'].queryset = self.get_pending_currencies()
        return context

    def form_valid(self, form):
        form.instance.user_insert = self.request.user
        form.save()
        return super(SettingCurrencyAdd, self).form_valid(form)

    def get_initial(self):
        return {'owner': self.request.user}

    def get_success_url(self):
        return reverse('budget:setting_currency')

    def get_pending_currencies(self):
        return Currency.objects.get_pending_currencies(self.request.user)


class SettingCurrencyUpdate(LoginRequiredMixin, UpdateView):
    template_name = "setting_currency_add.html"
    model = models.CurrencyUser
    form_class = CurrencyUserForm

    def get_context_data(self, **kwargs):
        context = super(SettingCurrencyUpdate, self).get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        form.instance.user_insert = self.request.user
        form.save()
        return super(SettingCurrencyUpdate, self).form_valid(form)

    def get_initial(self):
        return {'owner': self.request.user}

    def get_success_url(self):
        return reverse('budget:setting_currency')

    def get_pending_currencies(self):
        return Currency.objects.get_pending_currencies(self.request.user)

    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        obj = super(SettingCurrencyUpdate, self).get_object()
        if not obj.user_insert == self.request.user:
            raise Http404
        return obj


class SettingCurrencyDelete(LoginRequiredMixin, DeleteView):
    template_name = "setting_currency_delete.html"
    model = models.CurrencyUser
    form_class = CurrencyUserForm

    def get_success_url(self):
        return reverse('budget:setting_currency')

    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        obj = super(SettingCurrencyDelete, self).get_object()
        if not obj.user_insert == self.request.user:
            raise Http404
        return obj


class SettingCategory(LoginRequiredMixin, ListView):
    template_name = "setting_category.html"
    model = models.Category

    def get_queryset(self):
        queryset = self.model.objects.all_my_categories(self.request.user)
        return queryset


class SettingSubCategoryAdd(LoginRequiredMixin, CreateView):
    template_name = "setting_subcategory_add.html"
    model = models.SubCategory
    form_class = SubcategoryForm

    def get_context_data(self, **kwargs):
        context = super(SettingSubCategoryAdd, self).get_context_data(**kwargs)
        context['category'] = self.get_category()
        return context

    def form_valid(self, form):
        form.save()
        return super(SettingSubCategoryAdd, self).form_valid(form)

    def get_initial(self):
        return {'category': self.get_category()}

    def get_category(self):
        category = models.Category.objects.get(
            pk=int(self.kwargs.get('category_pk')))
        return category

    def get_success_url(self):
        return reverse('budget:setting_category')


class SettingSubCategoryUpdate(LoginRequiredMixin, UpdateView):
    template_name = "setting_subcategory_update.html"
    model = models.SubCategory
    form_class = SubcategoryForm

    def get_success_url(self):
        return reverse('budget:setting_category')

    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        obj = super(SettingSubCategoryUpdate, self).get_object()
        if not obj.category.user_insert == self.request.user:
            raise Http404
        return obj


class SettingSubCategoryDelete(LoginRequiredMixin, DeleteView):
    template_name = "setting_subcategory_delete.html"
    model = models.SubCategory
    form_class = SubcategoryForm

    def get_success_url(self):
        return reverse('budget:setting_category')

    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        obj = super(SettingSubCategoryDelete, self).get_object()
        if not obj.category.user_insert == self.request.user:
            raise Http404
        return obj
