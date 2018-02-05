from django.views.generic import ListView
from django.contrib.auth.mixins import (LoginRequiredMixin)
from apps.budget import models


class SettingCategory(LoginRequiredMixin, ListView):
    template_name = "setting_category.html"
    model = models.Category
