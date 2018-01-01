import factory


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'auth.User'  # Equivalent to ``model = myapp.models.User``
        django_get_or_create = ('username',)

    username = 'openbudget'
    password = factory.PostGenerationMethodCall('set_password', '12345678')
