# -*- coding: utf-8 -*-
from .base import FunctionalTest
from selenium.webdriver.support.ui import Select
from django.urls import reverse
from django.test.utils import override_settings
from apps.budget.tests.factories import TransactionFactory
from datetime import datetime


class TransactionTest(FunctionalTest):

    @override_settings(DEBUG=True)
    def test_empty_list_transactions(self):

        url_register = reverse('budget:transaction_list')
        self.browser.get(self.live_server_url + url_register)
        self.login()
        # If there are not accounts created, display a message
        display_text = self.browser.find_element_by_class_name(
            'msg_no_transactions').text

        self.assertIn(display_text, 'There are not transactions created')

    @override_settings(DEBUG=True)
    def test_create_transaction_success(self):

        url_add_account = reverse('budget:transaction_add')
        self.browser.get(self.live_server_url + url_add_account)
        self.login()

        category = Select(self.browser.find_element_by_id('id_category'))
        account = Select(self.browser.find_element_by_id('id_account'))
        amount = self.browser.find_element_by_id('id_amount')
        place = self.browser.find_element_by_id('id_place')
        currency = Select(self.browser.find_element_by_id('id_currency'))

        category.select_by_visible_text('Food')
        self.wait_for_select_fill('id_subcategory', 'Supermarket')
        amount.send_keys('340')
        currency.select_by_visible_text('USD')
        place.send_keys('Nacional')
        account.select_by_visible_text('Family Account')

        log_but2 = "//input[@class='btn btn-success']"
        self.browser.find_element_by_xpath(log_but2).click()

        date = datetime.now().strftime('%b/%d/%Y')

        text = 'Supermarket\nFamily Account Nacional ' + date + ' 340.00 USD'
        self.wait_for_row_in_list_table(text)

    @override_settings(DEBUG=True)
    def test_update_transaction_success(self):
        transaction_created = TransactionFactory()
        url_list = reverse('budget:transaction_list')
        self.browser.get(self.live_server_url + url_list)
        self.login()

        link_name = 'link-update-' + str(transaction_created.pk)
        self.browser.find_element_by_id(link_name).click()

        place = self.browser.find_element_by_id('id_place')
        place.clear()
        place.send_keys('pegaditos')

        log_but2 = "//input[@class='btn btn-success']"
        self.browser.find_element_by_xpath(log_but2).click()

        date = transaction_created.date_display
        text = 'Supermarket\nFamily Account pegaditos ' + date + ' 340.00 USD'
        self.wait_for_row_in_list_table(text)

    @override_settings(DEBUG=True)
    def test_delete_transaction_success(self):

        transaction_created = TransactionFactory()
        url_list = reverse('budget:transaction_list')
        self.browser.get(self.live_server_url + url_list)
        self.login()

        link_name = 'link-delete-' + str(transaction_created.pk)
        self.browser.find_element_by_id(link_name).click()

        log_but2 = "//input[@class='btn btn-danger']"
        self.browser.find_element_by_xpath(log_but2).click()

        text = 'There are not transactions created'
        self.wait_for_text_display(text)

    @override_settings(DEBUG=True)
    def test_view_only_my_transactions(self):

        transaction_created = TransactionFactory()
        url_list = reverse('budget:transaction_list')
        self.browser.get(self.live_server_url + url_list)
        self.login()

        date = transaction_created.date_display
        text = 'Supermarket\nFamily Account Supermercado Nacional '
        + date + ' 340.00 USD'
        self.wait_for_row_in_list_table(text)
