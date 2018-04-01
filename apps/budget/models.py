from django.db import models
from apps.utils import models as utils
from django.contrib.auth.models import User
from apps.budget import managers
from django.db.models import signals
import uuid
from apps.budget.services import RecurrentSheduleService, SheduleLineService


class CurrencyUser(utils.CommonInfo):
    owner = models.ForeignKey(User)
    currency = models.ForeignKey(utils.Currency)
    ratio = models.DecimalField(max_digits=10, decimal_places=6)
    inverse_ratio = models.DecimalField(max_digits=10, decimal_places=4)
    is_base = models.BooleanField(default=False)
    objects = managers.CurrencyManager()

    def __str__(self):
        return self.currency.name

    @property
    def description_inverse_ratio(self):
        if self.is_base:
            return "This is your base currency"
        else:
            msg = get_inverse_ratio_desc(self)
            return msg
            # return "This is not your base currency " + base_currency.currency


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
    css = models.CharField(max_length=30)
    color = models.ForeignKey(utils.Color)

    def __str__(self):
        return self.name


class Category(utils.CommonInfo):
    icon = models.ForeignKey(IconCategory)
    name = models.CharField(max_length=32)
    objects = managers.CategoryManager()

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    category = models.ForeignKey(Category, related_name='subcategories')
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
    currency = models.ForeignKey(utils.Currency)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    exchange = models.DecimalField(max_digits=10, decimal_places=2)
    place = models.CharField(max_length=128, blank=True, null=True)
    payee = models.CharField(max_length=128, blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    photo = models.FileField(upload_to='transactions', blank=True, null=True)
    date = models.DateTimeField()
    amount_account = models.DecimalField(max_digits=10, decimal_places=2,
                                         blank=True, null=True)
    objects = managers.TransactionManager()

    def __str__(self):
        return "{}-{}".format(self.subcategory, self.amount)

    @property
    def date_display(self):
        return self.date.strftime('%b/%d/%Y')

    @property
    def date_format(self):
        return self.date.strftime('%m/%d/%Y')


class PeriodType(models.Model):
    name = models.CharField(max_length=32)
    code = models.CharField(max_length=16, blank=True, null=True)

    def __str__(self):
        return self.name


class DayShedule(models.Model):
    period_type = models.ForeignKey(PeriodType)
    name = models.CharField(max_length=16)
    value = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class RecurrentTransaction(utils.CommonInfo):
    account = models.ForeignKey(Account)
    trx_type = models.ForeignKey(TransactionType)
    subcategory = models.ForeignKey(SubCategory)
    currency = models.ForeignKey(utils.Currency)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    exchange = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    place = models.CharField(max_length=128, blank=True, null=True)
    payee = models.CharField(max_length=128, blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    photo = models.FileField(upload_to='transactions', blank=True, null=True)
    objects = managers.RecurrentsManager()

    def __str__(self):
        return "{}-{}".format(self.subcategory, self.amount)


class RecurrentShedule(models.Model, RecurrentSheduleService):
    recurrent_transaction = models.ForeignKey(RecurrentTransaction,
                                              related_name='shedule')
    day = models.ForeignKey(DayShedule, blank=True, null=True)
    start_posting = models.DateField(blank=True, null=True)

    def __str__(self):
        return "{}".format(self.day)


class RecurrentSheduleLine(models.Model, SheduleLineService):
    shedule = models.ForeignKey(RecurrentShedule,
                                related_name='lines')
    et_date = models.DateField()
    log_post_date = models.DateField(blank=True, null=True)
    objects = managers.SheduleLineManager()

    def __str__(self):
        return "{}".format(self.et_date)


class RecurrentHistory(models.Model):
    recurrent_transaction = models.ForeignKey(RecurrentTransaction)
    date = models.DateField()


class BudgetYear(models.Model):
    value = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.value)


class Budget(utils.CommonInfo):
    name = models.CharField(max_length=64)
    year = models.ForeignKey(BudgetYear)
    period_type = models.ForeignKey(PeriodType)
    accounts = models.ManyToManyField(Account)
    owners = models.ManyToManyField(User, blank=True)
    currency = models.ForeignKey(utils.Currency, blank=True, null=True)
    objects = managers.BudgetManager()

    def __str__(self):
        return self.name


class BudgetPeriod(utils.CommonInfo):
    description = models.CharField(max_length=128)
    budget = models.ForeignKey(Budget, related_name='periods')
    init_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.description


class BudgetLine(models.Model):
    period = models.ForeignKey(BudgetPeriod, related_name='details')
    subcategory = models.ForeignKey(SubCategory)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.subcategory.name


class BudgetShareStatus(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class BudgetShareMember(utils.CommonInfo):
    budget = models.ForeignKey(Budget, related_name='shares')
    member = models.ForeignKey(User)
    status = models.ForeignKey(BudgetShareStatus)
    objects = managers.BudgetShareManager()
    token = models.UUIDField(primary_key=True,
                             default=uuid.uuid4,
                             editable=False)

    def __str__(self):
        return "{} - {}".format(self.budget, self.member)


class DurationFilter(models.Model):
    name = models.CharField(max_length=64)
    value = models.IntegerField()
    is_day = models.BooleanField(default=True)
    is_month = models.BooleanField(default=False)
    is_year = models.BooleanField(default=False)

    def __str__(self):
        return self.name


def get_inverse_ratio_desc(currency_user):
    base_currency = CurrencyUser.objects.get_my_base_currency(
        currency_user.user_insert)

    result = "1 " + base_currency.currency.name + " = "
    result = result + str(
        currency_user.inverse_ratio) + " " + currency_user.currency.name
    return result


from .signals import auto_period_register

signals.post_save.connect(auto_period_register, sender=Budget)
