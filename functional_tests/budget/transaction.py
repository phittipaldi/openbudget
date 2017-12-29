# -*- coding: utf-8 -*-
from .base import FunctionalTest
# from selenium.webdriver.support.ui import Select
from django.urls import reverse
# from django.test.utils import override_settings
# from apps.budget.tests.factories import AccountFactory


class TransactionTest(FunctionalTest):

    def test_empty_list_account(self):

        url_register = reverse('budget:transaction_list')
        self.browser.get(self.live_server_url + url_register)
        self.login()

        display_text = self.browser.find_element_by_class_name(
            'msg_no_transaction').text

        self.assertIn(display_text, 'There are not transactions created')
