# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest
from django.urls import reverse
# from unittest import skip


class LoginTest(FunctionalTest):

    def test_login_fail(self):

        url_login = reverse('accounts:login')
        self.browser.get(self.live_server_url + url_login)
        username_inputbox = self.browser.find_element_by_id('id_username')
        password_inputbox = self.browser.find_element_by_id('id_password')

        username_inputbox.send_keys('phittipadiX@gmail.com')
        password_inputbox.send_keys('tibaldix1234')

        password_inputbox.send_keys(Keys.ENTER)

        self.browser.implicitly_wait(3)
        error_text = self.browser.find_element_by_class_name('errorlist').text
        self.assertIn('enter a correct username and password', error_text)
