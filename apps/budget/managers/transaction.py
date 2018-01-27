from django.db import models
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


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

    def last_30_days_transactions(self, owner):
        date_now = datetime.today()
        init_date = date_now.today() - timedelta(days=30)
        filter_data = dict()
        filter_data['date__range'] = [init_date, date_now]
        filter_data['account__owners__in'] = [owner]
        return self.filter(**filter_data).order_by('-date')

    def transactions_by_duration(self, owner, duration):
        from apps.budget.models import DurationFilter
        dur_filt = DurationFilter.objects.get(pk=duration)
        date_now = datetime.today()
        if dur_filt.is_day:
            init_date = date_now.today() - timedelta(days=dur_filt.value)
        else:
            init_date = date_now.today() - relativedelta(months=dur_filt.value)

        filter_data = dict()
        filter_data['date__range'] = [init_date, date_now]
        filter_data['account__owners__in'] = [owner]
        return self.filter(**filter_data).order_by('-date')
