"""
Django settings for engine project.

Generated by 'django-admin startproject' using Django 1.11.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

from os.path import dirname, abspath, basename
from sys import path

from configurations import Configuration

from .logger_settings import LoggerSettingsMixin


class Settings(LoggerSettingsMixin, Configuration):

    # Absolute filesystem path to the Django project directory:
    DJANGO_ROOT = dirname(dirname(abspath(__file__)))
    # Absolute filesystem path to the top-level project folder:
    SITE_ROOT = dirname(DJANGO_ROOT)

    # Site name:
    SITE_NAME = basename(DJANGO_ROOT)

    ALLOWED_HOSTS = ['*']

    # Add our project to our pythonpath, this way we don't need to type our project
    # name in our dotted import paths:
    path.append(DJANGO_ROOT)

    # Quick-start development settings - unsuitable for production
    # See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = '49zo$w%0)nqh@x_51fpt(z+)#%*copgs^h@^5y%x=gojgtterl'

    # Application definition

    DJANGO_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
    ]

    THIRD_PARTY_APPS = []

    LOCAL_APPS = [
        'libs',
        'dark_matter.commons',
        'dark_matter.entities',
        'dark_matter.keywords',
        'dark_matter.search_engine'
    ]

    INSTALLED_APPS = property(lambda self: self.DJANGO_APPS + self.THIRD_PARTY_APPS + self.LOCAL_APPS)

    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]

    ROOT_URLCONF = 'engine.urls'

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [],
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

    WSGI_APPLICATION = 'engine.wsgi.application'

    # Password validation
    # https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
    # https://docs.djangoproject.com/en/1.11/topics/i18n/

    LANGUAGE_CODE = 'en-us'

    TIME_ZONE = 'UTC'

    USE_I18N = True

    USE_L10N = True

    USE_TZ = True

    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/1.11/howto/static-files/

    STATIC_URL = '/static/'
