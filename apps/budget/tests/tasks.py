from django.test import TestCase
from apps.utils.models import Currency
from apps.security.tests.factories import UserFactory
from .factories import AccountTypeFactory
from django.test import RequestFactory


class TestTaskMethods(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.account_type = AccountTypeFactory()
        self.currency = Currency.objects.create(name='USD')
        self.current_user = UserFactory(username='openbudget',
                                        password='12345678')
