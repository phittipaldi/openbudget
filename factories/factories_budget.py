import factory


class AccountTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'budget.AccountType'
        django_get_or_create = ('name',)

    name = 'General'
