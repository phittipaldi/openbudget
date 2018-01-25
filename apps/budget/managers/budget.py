from django.db import models


class BudgetManager(models.Manager):

    def all_my_budgets(self, owner):
        return self.filter(user_insert=owner)
