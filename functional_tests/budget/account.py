# -*- coding: utf-8 -*-
from .base import FunctionalTest
from selenium.webdriver.support.ui import Select
from django.urls import reverse
from django.test.utils import override_settings
# from unittest import skip

MAX_WAIT = 10


class AccountTest(FunctionalTest):

    def test_empty_list_account(self):

        url_register = reverse('budget:account_list')
        self.browser.get(self.live_server_url + url_register)
        # If there are not accounts created, display a message
        display_text = self.browser.find_element_by_class_name(
            'msg_no_accounts').text

        self.assertIn(display_text, 'There are not accounts created')

    @override_settings(DEBUG=True)
    def test_create_account_success(self):

        url_add_account = reverse('budget:account_add')
        self.browser.get(self.live_server_url + url_add_account)
        self.login()

        name = self.browser.find_element_by_id('id_name')
        account_type = Select(self.browser.find_element_by_id(
            'id_account_type'))
        amount = self.browser.find_element_by_id('id_starting_amount')
        currency = Select(self.browser.find_element_by_id('id_currency'))

        name.send_keys('Family Account')
        account_type.select_by_visible_text('General')
        amount.send_keys('5700')
        currency.select_by_visible_text('USD')

        log_but2 = "//input[@class='btn btn-success']"
        self.browser.find_element_by_xpath(log_but2).click()

        self.wait_for_row_in_list_table('Family Account General 5700.00 Edit Delete')

    @override_settings(DEBUG=True)
    def test_create_account_fail(self):

        url_add_account = reverse('budget:account_add')
        self.browser.get(self.live_server_url + url_add_account)
        self.login()

        name = self.browser.find_element_by_id('id_name')
        account_type = Select(self.browser.find_element_by_id(
            'id_account_type'))

        name.send_keys('Fun Time')
        account_type.select_by_visible_text('General')

        log_but2 = "//input[@class='btn btn-success']"
        self.browser.find_element_by_xpath(log_but2).click()
