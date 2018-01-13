from django.db import models


class TransactionManager(models.Manager):

    def all_my_transactions(self, owner):
        return self.filter(account__owners__in=[owner]).order_by('-date')
