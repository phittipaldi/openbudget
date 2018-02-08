from django.db import models


class CurrencyManager(models.Manager):

    def all_my_currencies(self, owner):
        return self.filter(user_insert=owner)
