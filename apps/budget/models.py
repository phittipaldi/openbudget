from django.db import models
from apps.utils import models as utils
from django.contrib.auth.models import User


class CurrencyUser(utils.CommonInfo):
    currency = models.ForeignKey(utils.Currency)
    ratio = models.DecimalField(max_digits=10, decimal_places=2)
    inverse_ratio = models.DecimalField(max_digits=10, decimal_places=2)
    is_base = models.BooleanField(default=False)

    def __str__(self):
        return self.currency.name


class AccountType(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Account(utils.CommonInfo):
    name = models.CharField(max_length=64)
    account_type = models.ForeignKey(AccountType)
    starting_amount = models.DecimalField(max_digits=10, decimal_places=2,
                                          default=0)
    currency = models.ForeignKey(utils.Currency)
    color = models.ForeignKey(utils.Color, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def balance(self):
        return self.starting_amount


class AccountOwner(utils.CommonInfo):
    account = models.ForeignKey(Account)
    owner = models.ForeignKey(User)
    is_principal = models.BooleanField(default=False)

    def __str__(self):
        return "{} - {}".format(self.owner.username, self.account)


class IconCategory(models.Model):
    name = models.CharField(max_length=30)
    color = models.ForeignKey(utils.Color)

    def __str__(self):
        return self.name


class Category(models.Model):
    icon = models.ForeignKey(IconCategory)
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class SubCategory(utils.CommonInfo):
    category = models.ForeignKey(Category)
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class TransactionType(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class Transactions(utils.CommonInfo):
    account = models.ForeignKey(Account)
    trx_type = models.ForeignKey(TransactionType)
    subcategory = models.ForeignKey(SubCategory)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    photo = models.FileField(upload_to='transactions')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}-{}".format(self.account, self.amount)
