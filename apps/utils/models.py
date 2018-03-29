from django.db import models
from django.contrib.auth.models import User
from apps.utils import managers


class CommonInfo(models.Model):
    user_insert = models.ForeignKey(
        User,
        related_name='user_insert_%(class)s',
        editable=True)
    user_update = models.ForeignKey(
        User,
        related_name='user_update_%(class)s',
        blank=True, null=True, editable=False)

    class Meta:
        abstract = True


class Color(models.Model):
    name = models.CharField(max_length=30)
    css = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Currency(CommonInfo):
    name = models.CharField(max_length=64, blank=True, null=True)
    description = models.CharField(max_length=120, blank=True, null=True)
    objects = managers.CurrencyManager()

    def __str__(self):
        return self.name + ' - ' + self.description


class CurrencyRate(models.Model):
    source = models.ForeignKey(Currency, related_name='rate')

    def __str__(self):
        return self.source.name


class CurrencyRateLine(models.Model):
    source = models.ForeignKey(CurrencyRate, related_name='quotes')
    quote = models.ForeignKey(Currency)
    value = models.DecimalField(max_digits=10, decimal_places=4)

    def __str__(self):
        return str(self.value)

    @property
    def description(self):

        result = "1 " + self.source.source.name + " = "
        result = result + str(self.value) + " " + self.quote.name
        return result


#https://free.currencyconverterapi.com/api/v5/convert?q=USD_PHP&compact=y
