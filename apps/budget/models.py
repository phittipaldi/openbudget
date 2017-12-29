from django.db import models
from apps.utils import models as utils
from django.contrib.auth.models import User
from apps.budget.managers import account as managers


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
    owners = models.ManyToManyField(User)
    starting_amount = models.DecimalField(max_digits=10, decimal_places=2,
                                          default=0)
    currency = models.ForeignKey(utils.Currency)
    color = models.ForeignKey(utils.Color, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    objects = managers.AccountManager()

    def __str__(self):
        return self.name

    def balance(self):
        return self.starting_amount


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


class Transaction(utils.CommonInfo):
    account = models.ForeignKey(Account)
    trx_type = models.ForeignKey(TransactionType)
    subcategory = models.ForeignKey(SubCategory)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payee = models.CharField(max_length=128, blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    photo = models.FileField(upload_to='transactions')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}-{}".format(self.account, self.amount)
