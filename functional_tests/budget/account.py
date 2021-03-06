# -*- coding: utf-8 -*-
from .base import FunctionalTest
from selenium.webdriver.support.ui import Select
from django.urls import reverse
from django.test.utils import override_settings
from apps.budget.tests.factories import AccountFactory
# from unittest import skip

MAX_WAIT = 10


class AccountTest(FunctionalTest):

    def test_empty_list_account(self):

        url_register = reverse('budget:account_list')
        self.browser.get(self.live_server_url + url_register)
        self.login()
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

        self.wait_for_row_in_list_table('Family Account General 5700.00')

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

    @override_settings(DEBUG=True)
    def test_update_account_success(self):
        account_created = AccountFactory()
        url_list_account = reverse('budget:account_list')
        self.browser.get(self.live_server_url + url_list_account)
        self.login()

        link_name = 'link-update-' + str(account_created.pk)
        self.browser.find_element_by_id(link_name).click()

        name = self.browser.find_element_by_id('id_name')
        name.clear()
        name.send_keys('Family Update')

        log_but2 = "//input[@class='btn btn-success']"
        self.browser.find_element_by_xpath(log_but2).click()

        text = 'Family Update General 0.00'
        self.wait_for_row_in_list_table(text)

    @override_settings(DEBUG=True)
    def test_delete_account_success(self):

        account_created = AccountFactory()
        url_list_account = reverse('budget:account_list')
        self.browser.get(self.live_server_url + url_list_account)
        self.login()

        link_name = 'link-delete-' + str(account_created.pk)
        self.browser.find_element_by_id(link_name).click()

        log_but2 = "//input[@class='btn btn-danger']"
        self.browser.find_element_by_xpath(log_but2).click()

        text = 'There are not accounts created'
        self.wait_for_text_display(text)

    @override_settings(DEBUG=True)
    def test_view_only_my_accounts(self):

        AccountFactory.create(owners=([self.current_user]))
        url_list_account = reverse('budget:account_list')
        self.browser.get(self.live_server_url + url_list_account)
        self.login()

        text = 'Family Account General 0.00'
        self.wait_for_row_in_list_table(text)
