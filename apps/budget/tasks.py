from celery.task.schedules import crontab
import datetime
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger
from .models import RecurrentShedule

logger = get_task_logger(__name__)


@periodic_task(run_every=(crontab(minute="*/1", day_of_week="*")))
def register_recurrent_transaction():
    logger.info("Starting post shedule transactions)")
    posting_pending_start_today()
    posting_pending_for_today()

    return "Registering recurrent transaction done..."


def posting_pending_start_today():

    recurrents = RecurrentShedule.objects.all_starts_today()

    for recurrent in recurrents:
        recurrent.post_transaction()
        recurrent.set_shedule_lines()


def posting_pending_for_today():

    recurrents = RecurrentShedule.objects.all_pending_today()

    for recurrent in recurrents:
        recurrent.post_transaction()
