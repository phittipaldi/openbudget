# -*- coding: utf-8 -*-
from django.conf import settings
from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
from apps.utils.models import Currency
from apps.security.tests.factories import UserFactory
from django.test import RequestFactory
from apps.budget.tests.factories import AccountTypeFactory
from ..management.commands.create_session import create_authenticated_session
import time

MAX_WAIT = 10


def wait(fn):
    def modified_fn(*args, **kwargs):
        start_time = time.time()
        while True:
            try:
                return fn(*args, **kwargs)
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)
    return modified_fn


class FunctionalTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
        self.factory = RequestFactory()
        self.account_type = AccountTypeFactory()
        Currency.objects.create(name='USD')
        UserFactory(username='openbudget',
                    password='12345678')

    def tearDown(self):
        self.browser.quit()

    def login(self):
        username_inputbox = self.browser.find_element_by_id('id_username')
        password_inputbox = self.browser.find_element_by_id('id_password')

        username_inputbox.send_keys('openbudget')
        password_inputbox.send_keys('12345678')

        password_inputbox.send_keys(Keys.ENTER)

        self.wait_to_be_logged_in('openbudget')

    @wait
    def wait_to_be_logged_in(self, username):
        self.browser.find_element_by_id('user-dropdown').click()
        self.browser.find_element_by_link_text('Logout')
        # navbar = self.browser.find_element_by_css_selector('.dropdown-user')
        navbar = self.browser.find_element_by_id('user-display')
        self.assertIn(username, navbar.text)

    @wait
    def wait_for(self, fn):
        return fn()

    @wait
    def wait_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    @wait
    def wait_for_errors_form(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def create_pre_authenticated_session(self, username):

        session_key = create_authenticated_session(username)

        self.browser.get(self.live_server_url + "/404_no_such_url/")
        self.browser.add_cookie(dict(
            name=settings.SESSION_COOKIE_NAME,
            value=session_key,
            path='/',
        ))
