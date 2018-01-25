from django.db import models


class CurrencyManager(models.Manager):

    def all_my_currencies(self, owner):
        from apps.budget.models import CurrencyUser
        currencies = CurrencyUser.objects.filter(owner=owner)
        return self.filter(
            id__in=[currency.currency.id for currency in currencies])
