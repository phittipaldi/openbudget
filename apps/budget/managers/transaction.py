from django.db import models


class TransactionManager(models.Manager):

    def all_my_transactions(self, owner):
        return self.filter(account__owners__in=[owner]).order_by('-date')

    def all_my_transactions_by_period(self, owner, period):
        filter_data = dict()
        filter_data['date__range'] = [period.init_date, period.end_date]
        filter_data['account__in'] = [owner]
        return self.filter(**filter_data).order_by('-date')

    def my_last_transactions(self, owner):
        return self.filter(account__owners__in=[owner]).order_by('-date')[:0]
