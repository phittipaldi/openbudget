# -*- coding: utf-8 -*-
from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
# from unittest import skip
# import time

MAX_WAIT = 10


class FunctionalTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()
