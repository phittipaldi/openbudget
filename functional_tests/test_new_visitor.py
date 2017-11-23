# -*- coding: utf-8 -*-
from .base import FunctionalTest
# from unittest import skip


class NewVisitorTest(FunctionalTest):

    def test_new_visitor(self):
        self.browser.get(self.live_server_url)
        self.assertIn('Open Budget', self.browser.title)
