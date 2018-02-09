from django.db import models


class CurrencyManager(models.Manager):

    def all_my_currencies(self, owner):
        from apps.budget.models import CurrencyUser
        currencies = CurrencyUser.objects.filter(owner=owner)
        return self.filter(
            id__in=[currency.currency.id for currency in currencies])

    def get_pending_currencies(self, owner):
        from apps.budget.models import CurrencyUser
        currencies = CurrencyUser.objects.filter(
            owner=owner).values('currency__pk')
        return self.exclude(pk__in=currencies)
