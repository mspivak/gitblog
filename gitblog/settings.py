"""
Django settings for gitblog project.

Generated by 'django-admin startproject' using Django 4.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path
import os

from dotenv import load_dotenv
load_dotenv(
    os.path.join(os.path.dirname(__file__), '../.env')
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-)m!lb23kalr534g-1d62o9v+f+-*#^0&nroo$gp&8&ux-8n9$2'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

DOMAIN = 'gitblog.link'

ALLOWED_HOSTS = [
    'localhost',
    'gitblog.link',
]

CSRF_TRUSTED_ORIGINS = [
    'http://localhost:8000',
]

INTERNAL_IPS = [
    "127.0.0.1",
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tailwind', 'theme', 'django_browser_reload',
    'gh',
    'users',
    'blogs',
    'pages',
    'storages',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_browser_reload.middleware.BrowserReloadMiddleware',
]

ROOT_URLCONF = 'gitblog.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

TAILWIND_APP_NAME = 'theme'

WSGI_APPLICATION = 'gitblog.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': os.environ.get('DB_HOST', '127.0.0.1'),
        'NAME': os.environ.get('DB_NAME', 'gitblog'),
        'USER': os.environ.get('DB_USER', 'mauro'),
        'PORT': os.environ.get('DB_PORT', '5432'),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
    }
}

# https://docs.djangoproject.com/en/4.0/topics/auth/customizing/#substituting-a-custom-user-model
# https://dev.to/earthcomfy/getting-started-custom-user-model-5hc
AUTH_USER_MODEL = 'users.User'

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/


AWS_DEFAULT_ACL = 'public-read'
AWS_USER_FILES_BUCKET_NAME = 'gitblog-user-files'
AWS_STORAGE_BUCKET_NAME = 'gitblog-static-files'
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'

STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATIC_ROOT = BASE_DIR / 'static'


# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

GITHUB_CLIENT_ID = os.getenv('GITHUB_CLIENT_ID')
GITHUB_CLIENT_SECRET = os.getenv('GITHUB_CLIENT_SECRET')
SELF_GITHUB_CLIENT_TOKEN = os.getenv('SELF_GITHUB_CLIENT_TOKEN')

