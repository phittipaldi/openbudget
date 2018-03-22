from django.db import models
import datetime


class RecurrentsManager(models.Manager):

    def all_my_recurrents(self, owner):
        return self.filter(user_insert__in=[owner])


class SheduleLineManager(models.Manager):

    def all_recurrents_pending(self):
        return self.filter(
            et_date__lte=datetime.date.today(),
            log_post_date__isnull=True)
