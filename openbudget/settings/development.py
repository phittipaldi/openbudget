# -*- coding: utf-8 -*-
from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

ACCOUNT_EMAIL_REQUIRED = False
ACCOUNT_EMAIL_VERIFICATION = False
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = False

INTERNAL_IPS = '127.0.0.1'

CURRENT_DOMAIN = 'http://127.0.0.1:8000'
# DEFAULT_FROM_EMAIL = "no-reply@getopenbudget.com "


EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'apikey'
EMAIL_HOST_PASSWORD = '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'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
