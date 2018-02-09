from django.views.generic.edit import (View)
from .models import CurrencyRateLine
from apps.budget.models import CurrencyUser
from django.http.response import JsonResponse
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
