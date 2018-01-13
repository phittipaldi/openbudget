import factory
from apps.security.tests.factories import UserFactory


class CurrencyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'utils.Currency'  # Equivalent to ``model = myapp.models.User``
        django_get_or_create = ('name',)

    name = 'USD'
    user_insert = factory.SubFactory(UserFactory)


class ColorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'utils.Color'  # Equivalent to ``model = myapp.models.User``
        django_get_or_create = ('name',)

    name = factory.Iterator(["Blue", "Red", "White"])
