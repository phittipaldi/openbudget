from django.views.generic.edit import (View)
from .models import CurrencyRateLine
from apps.budget.models import CurrencyUser
from django.http.response import JsonResponse
from django.views.generic.list import ListView
from apps.utils.forms import SearchForm
# Create your views here.


class CurrencyRateView(View):
    model = CurrencyRateLine

    def get(self, request, *args, **kwargs):

        source = CurrencyUser.objects.get(owner__pk=request.user.pk).currency
        ratio = self.model.objects.filter(
            quote__pk=self.kwargs.get('currency_pk'),
            source__source__pk=source.pk)[0]

        inverse_ratio = self.model.objects.filter(
            quote__pk=source.pk,
            source__source__pk=self.kwargs.get('currency_pk'))[0]

        result = ({"ratio": ratio.value, "inverse_ratio": inverse_ratio.value,
                   "ratio_desc": ratio.description,
                   "inverse_ratio_desc": inverse_ratio.description})

        return JsonResponse(result, safe=False)


class SearchListView(ListView):
    form_class = SearchForm
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(SearchListView, self).get_context_data(**kwargs)

        if 'form' not in context:
            context['form'] = self.form_class()

        if self.request.GET.items():
            context['form'] = self.form_class(self.request.GET)
            q = self.request.GET.get('q')
            if q is not None:
                context['query'] = q

        pb = self.request.GET.get('pb', self.paginate_by)
        context['pb'] = pb

        return context

    def get_paginate_by(self, queryset):
        """
        Paginate by specified value in querystring,
        or use default class property value.
        """
        return self.request.GET.get('pb', self.paginate_by)
