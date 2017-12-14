from django.test import TestCase
from apps.budget.models import Account
from apps.utils.models import Currency
from apps.security.tests.factories import UserFactory
from .factories import AccountTypeFactory
from django.test import RequestFactory


class AccountViewTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.account_type = AccountTypeFactory()
        self.currency = Currency.objects.create(name='USD')
        self.current_user = UserFactory(username='openbudget',
                                        password='12345678')
        self.client.login(username='openbudget', password='12345678')

    # Valid Form Data
    def test_account_empty_list(self):
        response = self.client.get('/budget/accounts/')
        self.assertEqual(Account.objects.count(), 0)
        expected_error = ("There are not accounts created")
        self.assertContains(response, expected_error)

    def test_success_add_account(self):
        data = {'name': "Family Account", 'currency': self.currency.pk,
                'account_type': self.account_type.pk,
                'starting_amount': 500,
                }

        response = self.client.post('/budget/account/add/', data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Account.objects.count(), 1)
