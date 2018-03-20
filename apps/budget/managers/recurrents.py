from django.db import models


class RecurrentsManager(models.Manager):

    def all_my_recurrents(self, owner):
        return self.filter(user_insert__in=[owner])
