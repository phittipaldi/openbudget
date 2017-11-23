# -*- coding: utf-8 -*-
from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest
from django.urls import reverse
# from unittest import skip


class RegisterTest(FunctionalTest):

    def test_register(self):

        url_register = reverse('accounts:register')
        self.browser.get(self.live_server_url + url_register)

        fullname_inputbox = self.browser.find_element_by_id('id_fullname')
        email_inputbox = self.browser.find_element_by_id('id_email')
        password1_inputbox = self.browser.find_element_by_id('id_password1')
        password2_inputbox = self.browser.find_element_by_id('id_password2')

        fullname_inputbox.send_keys('Tibaldi de Jesus')
        email_inputbox.send_keys('phittipaldi@gmail.com')
        password1_inputbox.send_keys('tibaldix1234')
        password2_inputbox.send_keys('tibaldix1234')
        password2_inputbox.send_keys(Keys.ENTER)

        self.browser.implicitly_wait(5)
        # self.assertIn('verification_sent', self.browser.current_url)
