from django.db import models


class CategoryManager(models.Manager):

    def all_my_categories(self, owner):
        return self.filter(user_insert=owner)

    def all_categories_account_owner(self, account):
        return self.filter(user_insert=account.user_insert)
