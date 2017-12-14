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
        display_text = self.browser.find_element_by_tag_name('h1').text

        self.assertIn(display_text, 'There are not accounts created')

    @override_settings(DEBUG=True)
    def test_create_account(self):

        # self.create_pre_authenticated_session('openbudget')

        url_add_account = reverse('budget:account_add')
        self.browser.get(self.live_server_url + url_add_account)
        self.login()

        name = self.browser.find_element_by_id('id_name')
        account_type = Select(self.browser.find_element_by_id(
            'id_account_type'))
        amount = self.browser.find_element_by_id('id_starting_amount')
        currency = Select(self.browser.find_element_by_id('id_currency'))

        name.send_keys('Family Account')
        account_type.select_by_value('1')
        amount.send_keys('5700')
        currency.select_by_value('1')

        log_but2 = "//input[@class='button-text']"
        self.browser.find_element_by_xpath(log_but2).click()

        self.wait_for_row_in_list_table('Family Account')
