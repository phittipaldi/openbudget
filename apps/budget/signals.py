from .models import BudgetPeriod
import calendar
from datetime import datetime


def auto_period_register(sender, instance, created=None, **kwargs):

    if instance.period_type.code == 'MONTHLY':
        register_periods_monthly(instance)


def register_periods_monthly(budget):

    for month in range(12):
        last_day = calendar.monthrange(budget.year.value, month + 1)[1]
        init_date = datetime(budget.year.value, month + 1, 1, 0, 0)
        end_date = datetime(budget.year.value, month + 1, last_day, 0, 0)
        month_string = str(init_date.strftime("%b"))
        description = month_string + "-" + str(budget.year.value)
        BudgetPeriod.objects.get_or_create(budget=budget,
                                           init_date=init_date,
                                           end_date=end_date,
                                           description=description,
                                           user_insert=budget.user_insert)
