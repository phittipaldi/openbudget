# -*- coding: utf-8 -*-
from apps.budget import models


def data_default_budget():

    models.AccountType.objects.get_or_create(name="Cash")
    models.AccountType.objects.get_or_create(name="General")
