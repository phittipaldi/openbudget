from celery.task.schedules import crontab
import requests
import datetime
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger
from .models import RecurrentSheduleLine
from apps.utils.models import Currency, CurrencyRateLine

logger = get_task_logger(__name__)


@periodic_task(run_every=(crontab(minute=0, hour='*/3', day_of_week="*")))
def register_recurrent_transaction():

    logger.info("Starting post shedule transactions)")

    recurrents = RecurrentSheduleLine.objects.all_recurrents_pending()

    for recurrent in recurrents:
        recurrent.post_transaction()
        recurrent.log_post_date = datetime.date.today()
        recurrent.save()
        recurrent.shedule.set_next_shedule_line()

    return "Registering recurrent transaction done..."


@periodic_task(run_every=(crontab(minute=0, hour='*/8')))
def update_currency_rate():
    logger.info("Starting updating currency rate")
    url_head = 'http://free.currencyconverterapi.com/api/v5/convert?q='

    currencies = Currency.objects.all()
    for currency in currencies:
        rate = currency.rate.all()[0]

        for currency in currencies:
            rate_code = rate.source.name + "_" + currency.name
            url = url_head + rate_code + '&compact=y'
            r = requests.get(url)
            data = r.json()
            valor = data.get(rate_code)['val']
            set_rate_lines(data, rate, currency, valor)


def set_rate_lines(data, currency_source, currency, valor):
    line = CurrencyRateLine.objects.get(
        source=currency_source,
        quote=currency)

    line.value = valor
    line.save()
    logger.info('line save...')
