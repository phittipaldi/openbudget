from django.db import models


class CurrencyManager(models.Manager):

    def all_my_currencies(self, owner):
        return self.filter(user_insert=owner)

    def get_my_base_currency(self, owner):
        return self.filter(owner=owner, is_base=True)[0]
