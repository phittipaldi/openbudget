# -*- coding: utf-8 -*-
from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse


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

    def tearDown(self):
        self.browser.quit()

    def test_login(self):
        url_login = reverse('security:login')
        self.browser.get(self.live_server_url + url_login)
