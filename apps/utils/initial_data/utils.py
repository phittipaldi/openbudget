# -*- coding: utf-8 -*-
from apps.utils import models


def data_default_utils():

    models.Currency.objects.get_or_create(name="USD")
    models.Currency.objects.get_or_create(name="DOP")
