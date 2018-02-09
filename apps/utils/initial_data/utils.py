# -*- coding: utf-8 -*-
from apps.utils import models
from .users import create_super_user


def data_default_utils():
    user = create_super_user()
    models.Currency.objects.get_or_create(name="USD",
                                          description="United States Dollar",
                                          user_insert=user)
    models.Currency.objects.get_or_create(name="DOP",
                                          description="Dominican Pesos",
                                          user_insert=user)
