from celery.task.schedules import crontab
import datetime
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger
from .models import RecurrentSheduleLine

logger = get_task_logger(__name__)


@periodic_task(run_every=(crontab(minute="*/1", day_of_week="*")))
def register_recurrent_transaction():

    logger.info("Starting post shedule transactions)")

    recurrents = RecurrentSheduleLine.objects.all_recurrents_pending()

    for recurrent in recurrents:
        recurrent.post_transaction()
        recurrent.log_post_date = datetime.date.today()
        recurrent.save()
        recurrent.shedule.set_next_shedule_line()

    return "Registering recurrent transaction done..."
