# -*- coding: utf-8 -*-
from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest
from django.urls import reverse
from unittest import skip


class AccountTest(FunctionalTest):

    def test_empty_list_account(self):

        url_register = reverse('budget:account_list')
        self.browser.get(self.live_server_url + url_register)
        # If there are not accounts created, display a message
        display_text = self.browser.find_element_by_tag_name('h1').text

        self.assertIn(display_text, 'There are not accounts created')

    @skip
    def test_create_account(self):
        # Click on the button
        # Introduce the corresponding data and click save
        pass

    @skip
    def test_list_account(self):
        # Display an account list with update and delete option
        pass
