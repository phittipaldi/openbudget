from django.db import models


class BudgetManager(models.Manager):

    def all_my_budgets(self, owner):
        return self.filter(owners__in=[owner])


class BudgetShareManager(models.Manager):

    def all_my_members_budget(self, owner, budget_pk):
        return self.filter(user_insert=owner, budget__pk=budget_pk)
