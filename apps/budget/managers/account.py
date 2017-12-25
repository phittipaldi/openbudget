from django.db import models


class AccountManager(models.Manager):

    def all_my_accounts(self, owner):
        return self.filter(owners__in=[owner])
