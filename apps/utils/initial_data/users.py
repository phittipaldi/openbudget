# -*- coding: utf-8 -*-
from django.contrib.auth.models import User


def create_super_user():

    try:
        user = User.objects.get(username='admin')
    except User.DoesNotExist:
        user = User.objects.create_superuser('admin',
                                             'phittipaldi@gmail.com',
                                             'cambiame123')

    return user
