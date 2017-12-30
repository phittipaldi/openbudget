# -*- coding: utf-8 -*-
from .base import FunctionalTest
from selenium.webdriver.support.ui import Select
from django.urls import reverse
from django.test.utils import override_settings
# from apps.budget.tests.factories import AccountFactory


class TransactionTest(FunctionalTest):

    def test_empty_list_account(self):

        url_register = reverse('budget:transaction_list')
        self.browser.get(self.live_server_url + url_register)
        self.login()

        display_text = self.browser.find_element_by_class_name(
            'msg_no_transaction').text

        self.assertIn(display_text, 'There are not transactions created')

    @override_settings(DEBUG=True)
    def test_create_account_success(self):

        url_add_account = reverse('budget:transaction_add')
        self.browser.get(self.live_server_url + url_add_account)
        self.login()

        account = Select(self.browser.find_element_by_id('id_account'))
        id_trx_type = Select(self.browser.find_element_by_id('id_trx_type'))
        amount = self.browser.find_element_by_id('id_amount')
        currency = Select(self.browser.find_element_by_id('id_currency'))
        category = Select(self.browser.find_element_by_id('id_category'))
        subcategory = Select(self.browser.find_element_by_id('id_subcategory'))

        name.send_keys('Family Account')
        account_type.select_by_visible_text('General')
        amount.send_keys('5700')
        currency.select_by_visible_text('USD')

        log_but2 = "//input[@class='btn btn-success']"
        self.browser.find_element_by_xpath(log_but2).click()

        self.wait_for_row_in_list_table('Family Account General 5700.00 Edit Delete')

    account = models.ForeignKey(Account)
    trx_type = models.ForeignKey(TransactionType)
    subcategory = models.ForeignKey(SubCategory)
    amount = models.DecimalField(max_digits=10, decimal_places=2)