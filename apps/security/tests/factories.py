import factory


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'auth.User'  # Equivalent to ``model = myapp.models.User``
        # django_get_or_create = ('username', 'password')

    username = 'john'
    password = factory.PostGenerationMethodCall('set_password', '1234567')
