from django.test import TestCase
from datetime import datetime
from apps.budget import models
from apps.security.tests.factories import UserFactory
from apps.utils.tests.factories import CurrencyFactory, ColorFactory
from .factories import (AccountTypeFactory, AccountFactory,
                        IconCategoryFactory, CategoryFactory,
                        TransactionTypeFactory, SubCategoryFactory)


class ModelTest(TestCase):

    def setUp(self):
        self.current_user = UserFactory(username='openbud')
        self.currency = CurrencyFactory(name='USD')
        self.account_type = AccountTypeFactory()

    def test_currency_user(self):
        object_created = models.CurrencyUser.objects.create(
            currency=self.currency,
            user_insert=self.current_user,
            is_base=True,
            ratio=1,
            inverse_ratio=1)

        self.assertEqual(str(object_created), 'USD')

    def test_account_type(self):
        object_created = models.AccountType.objects.create(
            name='Cash')
        self.assertEqual(str(object_created), 'Cash')

    def test_account(self):
        object_created = models.Account.objects.create(
            user_insert=self.current_user,
            name='Family Account',
            account_type=self.account_type,
            currency=self.currency,
            color=ColorFactory(name='Blue'))

        self.assertEqual(str(object_created.color), 'Blue')
        self.assertEqual(object_created.is_active, True)

    def test_account_owner(self):
        object_created = models.AccountOwner.objects.create(
            account=AccountFactory(),
            owner=self.current_user,
            user_insert=self.current_user)

        self.assertEqual(str(object_created),
                         self.current_user.username + ' - Family Account')
        self.assertEqual(object_created.is_principal, False)

    def test_icon_category(self):
        object_created = models.IconCategory.objects.create(
            name='Food',
            color=ColorFactory())

        self.assertEqual(str(object_created), 'Food')

    def test_category(self):
        object_created = models.Category.objects.create(
            name='Food',
            icon=IconCategoryFactory())

        self.assertEqual(str(object_created), 'Food')

    def test_subcategory(self):
        object_created = models.SubCategory.objects.create(
            name='Bar & Restaurant',
            category=CategoryFactory(),
            user_insert=self.current_user)

        self.assertEqual(str(object_created), 'Bar & Restaurant')

    def test_transaction_type(self):
        object_created = models.TransactionType.objects.create(
            name="Expense")

        self.assertEqual(str(object_created), 'Expense')

    def test_transaction(self):
        object_created = models.Transactions.objects.create(
            account=AccountFactory(),
            trx_type=TransactionTypeFactory(),
            subcategory=SubCategoryFactory(),
            amount=100,
            user_insert=self.current_user)

        self.assertEqual(object_created.date.date(), datetime.now().date())
