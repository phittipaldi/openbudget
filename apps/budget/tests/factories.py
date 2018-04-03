import factory
from apps.utils.tests.factories import CurrencyFactory, ColorFactory
from apps.security.tests.factories import UserFactory
from datetime import datetime


class AccountTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'budget.AccountType'
        django_get_or_create = ('name',)

    name = 'General'


class AccountFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'budget.Account'

    name = 'Family Account'
    account_type = factory.SubFactory(AccountTypeFactory)
    currency = factory.SubFactory(CurrencyFactory)
    color = factory.SubFactory(ColorFactory)
    user_insert = factory.SubFactory(UserFactory)

    @factory.post_generation
    def owners(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if self.user_insert:
            self.owners.add(self.user_insert)
        # if extracted:
        #     # A list of groups were passed in, use them
        #     for owner in extracted:
        #         self.owners.add(owner)


class IconCategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'budget.IconCategory'
        django_get_or_create = ('name', 'color',)

    name = 'Food'
    color = factory.SubFactory(ColorFactory)


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'budget.Category'
        django_get_or_create = ('name', 'icon',)

    name = 'Food'
    icon = factory.SubFactory(IconCategoryFactory)


class SubCategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'budget.SubCategory'
        django_get_or_create = ('name', 'category',)

    name = 'Supermarket'
    category = factory.SubFactory(CategoryFactory)
    user_insert = factory.SubFactory(UserFactory)


class TransactionTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'budget.TransactionType'
        django_get_or_create = ('name',)

    name = 'Expense'


class CurrencyUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'budget.CurrencyUser'

    owner = factory.SubFactory(UserFactory)
    currency = factory.SubFactory(CurrencyFactory)
    ratio = 1
    inverse_ratio = 1
    user_insert = factory.SubFactory(UserFactory)


class TransactionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'budget.Transaction'

    account = factory.SubFactory(AccountFactory)
    trx_type = factory.SubFactory(TransactionTypeFactory)
    subcategory = factory.SubFactory(SubCategoryFactory)
    currency = factory.SubFactory(CurrencyFactory)
    amount = 340
    exchange = 1
    place = 'Supermercado Nacional'
    user_insert = factory.SubFactory(UserFactory)
    date = datetime.now()


class PeriodTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'budget.PeriodType'

    name = 'Last'
    value = 'last_day'
