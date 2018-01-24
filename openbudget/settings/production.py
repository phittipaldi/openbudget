# -*- coding: utf-8 -*-
from .base import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': get_env_variable('MYSQL_DB'),
        'USER': get_env_variable('MYSQL_USER'),
        'PASSWORD': get_env_variable('MYSQL_PWD'),
        'HOST': get_env_variable('MYSQL_HOST'),
        'PORT': get_env_variable('MYSQL_PORT'),
        'OPTIONS': {
            'sql_mode': 'traditional',
        }
    }
}

CURRENT_DOMAIN = 'http://openbudget.cloudya.com.do'
ACCOUNT_EMAIL_REQUIRED = False
ACCOUNT_EMAIL_VERIFICATION = False
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = False
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

INTERNAL_IPS = '127.0.0.1'
