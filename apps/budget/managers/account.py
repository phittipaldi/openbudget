from django.db import models


class AccountManager(models.Manager):

    def all_my_accounts(self, owner):
        return self.filter(owners__in=[owner])

    def all_my_accounts_currency(self, owner, currency):
        return self.filter(owners__in=[owner], currency__pk=currency)
