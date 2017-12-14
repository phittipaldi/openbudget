from django.test import TestCase
from ..forms import AccountTransactionForm
from apps.budget.models import AccountType
from apps.utils.models import Currency
from apps.security.tests.factories import UserFactory
from .factories import AccountTypeFactory


class AccountFormTest(TestCase):

    def setUp(self):
        self.account_type = AccountTypeFactory()
        self.currency = Currency.objects.create(
            name='USD')
        self.current_user = UserFactory(username='openbud')

    # Valid Form Data
    def test_form_account_valid(self):
        form = AccountTransactionForm({'name': "Family Account",
                                       'account_type': self.account_type.pk,
                                       'starting_amount': 5000,
                                       'currency': self.currency.pk,
                                       'user_insert': self.current_user, })
        self.assertTrue(form.is_valid())

    def test_form_account_invalid(self):
        form = AccountTransactionForm({'name': "Family Account",
                                       'account_type': self.account_type.pk,
                                       'starting_amount': 5000,
                                       })

        self.assertFalse(form.is_valid())
