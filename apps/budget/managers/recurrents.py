from django.db import models
import datetime


class RecurrentsManager(models.Manager):

    def all_my_recurrents(self, owner):
        return self.filter(user_insert__in=[owner])

    def all_starts_today(self):

        return self.filter(
            is_pending=True,
            start_posting__lte=datetime.date.today())
