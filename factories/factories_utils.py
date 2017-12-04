import factory


class CurrencyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'utils.Currency'  # Equivalent to ``model = myapp.models.User``
        django_get_or_create = ('name',)

    name = 'USD'


class ColorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'utils.Color'  # Equivalent to ``model = myapp.models.User``
        django_get_or_create = ('name',)

    name = factory.Iterator(["Blue", "Red", "White"])
