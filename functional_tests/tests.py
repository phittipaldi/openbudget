# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
# from unittest import skip


class NewVisitorTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_new_visitor(self):
        self.browser.get(self.live_server_url)
        self.assertIn('openBudget', self.browser.title)


class LoginTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        url_login = reverse('security:login')
        self.browser.get(self.live_server_url + url_login)

    def tearDown(self):
        self.browser.quit()

    def test_login_fail(self):

        username_inputbox = self.browser.find_element_by_id('id_username')
        password_inputbox = self.browser.find_element_by_id('id_password')

        username_inputbox.send_keys('phittipadiX@gmail.com')
        password_inputbox.send_keys('tibaldix1234')

        password_inputbox.send_keys(Keys.ENTER)

        self.browser.implicitly_wait(3)
        error_text = self.browser.find_element_by_class_name('errorlist').text
        self.assertIn('enter a correct username and password', error_text)


class RegisterTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        url_register = reverse('security:register')
        self.browser.get(self.live_server_url + url_register)

    def tearDown(self):
        self.browser.quit()

    def test_register(self):

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
        # self.assertIn('account_activation_sent', self.browser.current_url)
