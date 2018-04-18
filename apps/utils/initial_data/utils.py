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

    models.Color.objects.get_or_create(name='Red',
                                       bg_code="rgba(255, 99, 132, 0.2)",
                                       border_code="rgba(255,99,132,1)",
                                       css='danger')

    models.Color.objects.get_or_create(name='Yellow',
                                       bg_code="rgba(255, 206, 86, 0.2)",
                                       border_code="rgba(255, 206, 86, 1)",
                                       css='default')

    models.Color.objects.get_or_create(name='Blue',
                                       bg_code="rgba(54, 162, 235, 0.2)",
                                       border_code="rgba(54, 162, 235, 1)",
                                       css='default')

    models.Color.objects.get_or_create(name='Green',
                                       bg_code="rgba(75, 192, 192, 0.2)",
                                       border_code="rgba(75, 192, 192, 1)",
                                       css='success')

    models.Color.objects.get_or_create(name='Dark Green',
                                       bg_code="rgba(0,255,0,0.3)",
                                       border_code="rgba(0,255,0,1))",
                                       css='success')

    models.Color.objects.get_or_create(name='Orange',
                                       bg_code="rgba(255, 159, 64, 0.2)",
                                       border_code="rgba(255, 159, 64, 0.2)",
                                       css='warning')
