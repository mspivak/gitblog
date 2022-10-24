from .settings import *
from django.conf import global_settings

DEBUG = True

DOMAIN = 'localhost:8000'

ALLOWED_HOSTS = ALLOWED_HOSTS + [
    '.ngrok.io',
]

CSRF_TRUSTED_ORIGINS = CSRF_TRUSTED_ORIGINS + [
    'https://735c-139-47-116-160.eu.ngrok.io'
]

INSTALLED_APPS = INSTALLED_APPS + [
    'django_extensions'
]

# Override production's s3 static files
STATIC_URL = 'static/'
STATICFILES_STORAGE = global_settings.STATICFILES_STORAGE