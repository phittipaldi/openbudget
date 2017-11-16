# -*- coding: utf-8 -*-
from django.views.generic import TemplateView
from django.contrib.auth.mixins import (LoginRequiredMixin)


class HomePage(TemplateView):
    template_name = "home.html"


class DashboardPage(LoginRequiredMixin, TemplateView):
    template_name = "home.html"
