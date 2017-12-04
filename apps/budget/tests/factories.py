import factory
from apps.utils.tests.factories import CurrencyFactory, ColorFactory
from apps.security.tests.factories import UserFactory


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
