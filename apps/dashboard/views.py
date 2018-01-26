# -*- coding: utf-8 -*-
from django.views.generic import TemplateView
from django.contrib.auth.mixins import (LoginRequiredMixin)


# class HomePage(LoginRequiredMixin, TemplateView):
#     template_name = "dashboard_old.html"


# class DashboardPage(LoginRequiredMixin, TemplateView):
#     template_name = "dashboard_old.html"


class DashboardPage(LoginRequiredMixin, TemplateView):
    template_name = "dashboard.html"
