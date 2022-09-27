from .settings import *
from django.conf import global_settings

DEBUG = True

INSTALLED_APPS = INSTALLED_APPS\
    + [
        'django_extensions'
    ]

# Override production's s3 static files
STATIC_URL = 'static/'
STATICFILES_STORAGE = global_settings.STATICFILES_STORAGE